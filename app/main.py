import logging
import traceback
import concurrent.futures

from dotenv import load_dotenv

from app.common.utils import *
from app.services.audio_transcribe import *
from app.services.data_processing import Data_processing
from app.services.emotion_detection import EmotionDetection
from app.services.face_recognition import verify_person_in_video

load_dotenv()

logging.basicConfig(level=logging.INFO, force=True)
logger = logging.getLogger(__name__)


def __process_audio(video_path: str, audio_path: str, subject: str):
    audio_extraction_status = Data_processing(video_path=video_path, audio_path=audio_path)

    if audio_extraction_status:
        logger.info("Audio extraction successful")
        txt = transcribe(audio_path=audio_path, subject=subject)
        if txt == "":
            raise Exception('No utterances found!!')
    else:
        raise Exception('Audio extraction Failed!!')

    return txt


def __similarity_score(txt, dic):
    try:
        similarity_score, introduction_score, adaptability_score, communication_score, \
            feedback_handling_score, overall_score, detailed_feedback = analyze_transcript(txt=txt, dic=dic, logger=logger)
    except:
        print(traceback.format_exc())
        similarity_score = 0
        introduction_score = 0
        adaptability_score = 0
        communication_score = 0
        feedback_handling_score = 0
        overall_score = 0
        detailed_feedback = {}
    return {'similarity_score': similarity_score, 'introduction_score': introduction_score,
            'adaptability_score': adaptability_score, 'communication_score': communication_score,
            'feedback_handling_score': feedback_handling_score, 'overall_score': overall_score,
            'detailed_feedback': detailed_feedback}

def __grammar_score(txt, demo_content):
    # Calculate grammar score
    grammar_score = grammer_score_func(txt=txt, demo_content=demo_content, logger=logger)
    return {'grammar_score': grammar_score}


def __cv_task_handler(video_path):
    emotion_dictionary = video_capture(emotion_function=EmotionDetection, video_path=video_path, logger=logger)
    emotion_score_value = emotion_score(emotion_dictionary=emotion_dictionary, logger=logger)
    return {'emotion_score': emotion_score_value}


def __format_output(future_lst):
    confidence = future_lst.get('confidence', 0)
    similarity_score = future_lst.get('similarity_score', 0)
    introduction_score = future_lst.get('introduction_score', 0)
    grammar_score = future_lst.get('grammar_score', 0)
    adaptability_score = future_lst.get('adaptability_score', 0)
    communication_score = future_lst.get('communication_score', 0)
    emotion_score = future_lst.get('emotion_score', 0)
    feedback_handling_score = future_lst.get('feedback_handling_score', 0)
    isSamePerson = future_lst.get('isSamePerson', False)

    response_lst = {
        'confidence': confidence if confidence > 0 else 0,
        'knowledge_score': similarity_score if similarity_score > 0 else 0,
        'introduction_score': introduction_score if introduction_score > 0 else 0,
        'emotion_score': emotion_score if emotion_score > 0 else 0,
        'grammar_score': grammar_score if grammar_score > 0 else 0,
        'adaptability_score': adaptability_score if adaptability_score > 0 else 0,
        'communication_score': communication_score if communication_score > 0 else 0,
        'feedback_handling_score': feedback_handling_score if feedback_handling_score > 0 else 0,
        'isSamePerson': isSamePerson
    }
    return response_lst


def main(video_path: str, audio_path: str, demo_content: dict, ref_image_path: str):
    """
    Args:
        video_path (str): Path of the video file
        audio_path (str): Path of the audio file to save in a specific directory
    """
    try:
        future_lst = {}
        futures = []

        executor = concurrent.futures.ThreadPoolExecutor(2)

        transcription = executor.submit(__process_audio, video_path, audio_path, demo_content.get('subject',''))
        future_1 = executor.submit(__cv_task_handler, video_path)
        futures.append(future_1)

        concurrent.futures.wait([transcription])
        txt = transcription.result()

        future_2 = executor.submit(confidence_retrival, txt, audio_path, logger)
        futures.append(future_2)
        future_3 = executor.submit(__similarity_score, txt, demo_content)
        futures.append(future_3)
        future_4 = executor.submit(__grammar_score, txt, demo_content)
        futures.append(future_4)
        future_5 = executor.submit(verify_person_in_video, video_path, "app/data/temp_frames", ref_image_path, threshold=0.2)
        futures.append(future_5)

        concurrent.futures.wait(futures)
        for future in futures:
            future_lst.update(future.result())

        response_lst = __format_output(future_lst)
        return response_lst

    except Exception:
        logger.error(traceback.format_exc())
        return {
            'confidence': 0,
            'knowledge_score': 0,
            'introduction_score': 0,
            'adaptability_score': 0,
            'grammar_score': 0,
            'emotion_score': 0,
            'communication_score': 0,
            'feedback_handling_score': 0,
            'isSamePerson': False
        }
