def knowledge_prompt(txt: str, subject: str, level: str, topic: str):
    query_string = ""

    if subject.lower() == 'hindi':
        level_dict = {
            'foundational': 'कक्षा 1 से 2 तक',
            'preparatory': 'कक्षा 3 से 5 तक',
            'middle': 'कक्षा 6 से 8 तक',
            'secondary': 'कक्षा 9 से 10 तक',
            'senior secondary': 'कक्षा 11 से 12 तक'
        }

        query_string += level_dict.get(level, '')

        if subject:
            query_string = query_string + ' ' + str(subject)

        prompt = f"""अभ्यर्थी ने {query_string} शिक्षक पद के लिए आवेदन किया था, तथा उसे "{topic}" विषय दिया गया था। यदि उम्मीदवार का भाषण विषय को कवर नहीं कर रहा है, तो knowledge_score 0 रखें। 
                            (If the candidate's speech is not covering the topic, or is in any other language or subject keep the knowledge_score 0)
                            दिए गए विषय पर उम्मीदवार के ज्ञान का मूल्यांकन करें, और नीचे JSON भरें,
                                   {{
                                        "topic_given": "string",
                                        "topic_explained": "string"
                                        "knowledge_score": [0-10] (Rating of how well the candidate is able to explain the given topic on a scale of 0-10, do not reduce rating for indirect examples. Do not assess strictly),
                                        "reason": "Reason for the above evaluation",
                                        "name_provided":  [BOOLEAN] (True if the candidate has given their name),
                                        "current_location_provided":  [BOOLEAN] (True if the candidate has provided their current working location where they are situated),
                                        "current_org_provided":  [BOOLEAN] (True if the candidate has given information or name of organisation they are working),
                                        "example_provided":  [BOOLEAN] (True if there are any examples used to explain the concepts or topics),
                                        "metaphor_provided":  [BOOLEAN] (True if there are any metaphors used to explain the concepts or topics),
                                        "analogy_provided":  [BOOLEAN] (True if there are any analogies used to explain the concepts or topics),
                                        "role_provided":  [BOOLEAN] (True if the candidate has explained their current roles and responsibilty at work, like what subject they are teaching),
                                        "summary_given": [BOOLEAN] (True if the candidate has summarised their session and covered all the points disscussed at the end)
                                        "bloom_tag_list": [LIST] (List of unique bloom tags covered in speech, based on blooms taxonomy for education)
                                   }}
    
                                   Speech: {txt}"""
    else:
        level_dict = {
            '': '',
            'foundational': 'grade 1 and 2',
            'preparatory': 'grade 3 to 5',
            'middle': 'grade 6 to 8',
            'secondary': 'grade 9 and 10',
            'senior secondary': 'grade 11 and 12'
        }

        query_string += level_dict.get(level, '')

        if subject:
            query_string = query_string + ' ' + str(subject)

        prompt = f"""The candidate has applied as {query_string} teacher position, and was given the topic of "{topic}".
                      If the candidate's speech is not covering the topic, keep the knowledge_score 0.
                      evaluate candidates knowledge on the given topic, and fill the JSON below,
                      {{
                          "topic_given": "string",
                          "topic_explained": "string"
                          "knowledge_score": [0-10] (Rating of how well the candidate is able to explain the given topic on a scale of 0-10, do not reduce rating for indirect examples. Do not assess strictly),
                          "reason": "Reason for the above evaluation",
                          "name_provided":  [BOOLEAN] (True if the candidate has given their name),
                          "current_location_provided":  [BOOLEAN] (True if the candidate has provided their current working location where they are situated),
                          "current_org_provided":  [BOOLEAN] (True if the candidate has given information or name of organisation they are working),
                          "example_provided":  [BOOLEAN] (True if there are any examples used to explain the concepts or topics),
                          "metaphor_provided":  [BOOLEAN] (True if there are any metaphors used to explain the concepts or topics),
                          "analogy_provided":  [BOOLEAN] (True if there are any analogies used to explain the concepts or topics),
                          "role_provided":  [BOOLEAN] (True if the candidate has explained their current roles and responsibilty at work, like what subject they are teaching),
                          "summary_given": [BOOLEAN] (True if the candidate has summarised their session and covered all the points disscussed at the end)
                          "bloom_tag_list": [LIST] (List of unique bloom tags covered in speech, based on blooms taxonomy for education)
                      }}

                     Speech: {txt}"""
    return prompt


def grammer_prompt(txt: str, subject: str):
    if subject.lower() == 'hindi':
        return f"निम्नलिखित भाषण के व्याकरण स्कोर को 0-10 के पैमाने पर रेट करें। आपको केवल एक संख्या प्रदान करना है, इसके अलावा कुछ नहीं। भाषण: {txt}"
    else:
        return f"Rate the grammar score of the following speech on scale of 0-10. YOU WILL ONLY RETURN A INTEGER, WHICH IS THE SCORE. NOTHING ELSE. Speech: {txt}."

def knowledge_prompt_non_acedamics(txt: str, subject: str, role: str, gen_answer: str):
    
    prompt = f"""The candidate has applied as for {role} as a {subject} position for acedamic and non-acedamic staff.
                    You are an expert evaluator assessing interview responses for a role in {subject}. Your 
                    task is to compare an AI-generated model answer with the candidate's answer and assign 
                    scores based on predefined criteria. The evaluation should consider accuracy, clarity, 
                    relevance, depth, and overall effectiveness of the response.

                    The candidate's response:
                    {txt}
                    
                    The AI-generated model answer:
                    {gen_answer}

                    **Scoring Breakdown**
                    Each score is rated on a 0 to 10 scale, where:
                    - 0-3 (Poor): Incomplete, off-topic, or lacks coherence.
                    - 4-6 (Average): Somewhat relevant but lacks depth, clarity, or structure.
                    - 7-8 (Good): Well-structured, relevant, and clear with minor areas for improvement.
                    - 9-10 (Excellent): Exceptional response with strong examples, deep insights, and clarity.
                    
                    **Check whether all the questions are answered in the response and if the response is relevant to the role**
                    1. Tell us about yourself.
                    2. What do you know about Ampersand Group?
                    3. What are your strengths and weaknesses?
                    4. Why are you looking for a change?
                    5. How do you prioritize tasks in multiple projects?
                    6. How do you stay organized and manage workloads?
                    7. How do you handle and grow from feedback?
                    
                    Score Categories Explained
                    1. Knowledge Score (0-10)
                    - Evaluates the depth of understanding in {subject}.
                    - Checks for factual correctness, industry awareness, and expertise.
                    
                    2. Introduction Score (0-10)
                    - Assesses how well the candidate introduces themselves.
                    - Looks at engagement, clarity, and relevance to the role.
                    
                    3. Adaptability Score (0-10)
                    - Measures flexibility in learning and handling changes.
                    - Evaluates responses to challenges or shifts in work environment.
                    
                    4. Feedback Handling Score (0-10)
                    - Measures openness to constructive criticism.
                    - Looks at how well the candidate applies feedback for improvement.

                    Generate a JSON output in the following format:                        
                    {{
                        "knowledge_score": [0-10],          # Evaluation of the introduction, clarity, and engagement.  
                        "introduction_score": [0-10],       # Assessment of industry knowledge, technical depth, and relevance.
                        "adaptability_score": [0-10],       # How well the candidate demonstrates flexibility and learning ability.
                        "feedback_handling_score": [0-10],  # Assessment of how the candidate receives and applies feedback.
                    }}
                    
                    **GENERATE THE ANSWER IN THE FOLLOWING JSON FORMAT ONLY - NO FURTHER EXPLAINATNION NEEDED**
                """
    return prompt

def gen_answer_prompt_func(subject: str):
    return f"""
        You are an experienced professional in the field of {subject}, preparing for an interview with the Ampersand Group. 
        Your responses should be well-structured, professional, and tailored to the role within {subject} that you are applying
        for. Answer the following questions in a clear and concise manner, providing relevant examples where necessary. 
        Ensure that your responses align with the company's values, industry standards, and best practices in {subject}.

        The questions to answer, in the given sequence, are:*

        1. Tell us about yourself.

        - Provide a brief professional background in {subject}, including your experience, skills, and achievements relevant to the role.
          Highlight your career progression and areas of expertise within {subject}.
        - Keep it concise and engaging.
        
        2. What do you know about Ampersand Group?

        - Research and summarize key information about the Ampersand Group, such as their industry, mission, values, and recent accomplishments.
        - Explain why you are interested in working for this company in the context of {subject}.
        
        3.What are your strengths and weaknesses?

        - Identify 2-3 strengths that are critical in {subject} and provide examples of how they have benefited your work.
        - Mention 1-2 weaknesses, but frame them as areas for improvement with examples of how you are working to overcome them in {subject}.
        
        4. Why are you looking for a change?

        - Provide a professional and positive reason for seeking a change, emphasizing your desire for career growth, new challenges, or better alignment with your long-term goals in {subject}.
        - Focus on how this change supports your personal and professional development, rather than any dissatisfaction with your current or past situations in {subject}.
        
        5. How do you prioritize tasks in multiple projects?

        - Describe your approach to prioritization in {subject}, such as using frameworks like Eisenhower Matrix, Agile methodologies, or industry-specific strategies.
        - Provide an example of a time when you effectively managed multiple projects in {subject}.
        
        6. How do you stay organized and manage your workload?

        - Explain the tools, techniques, or strategies you use to stay organized in {subject}, such as task management apps, scheduling methods, or workflow automation.
        - Give an example of how your organizational skills have helped you meet deadlines and maintain efficiency in {subject}.
        
        7.How do you handle and grow from feedback?

        - Demonstrate a growth mindset by explaining how you actively seek and apply feedback in {subject}.
        - Provide an example of a time when feedback helped you improve and contribute to success in {subject}.
        
        Instructions to generate the response:
        - Do not include the questions in your response.
        - Answer each question in a separate paragraph.
        - Use professional language and tone.
        - Provide specific examples and details to support your answers.
        - Keep your responses concise and relevant to the role within {subject}.
        - Ensure that your answers reflect your knowledge, skills, and experience in {subject}.
        - Aim to impress the interviewers with your expertise and professionalism in {subject}.
        - Review and revise your responses for clarity, accuracy, and alignment with the Ampersand Group's values and expectations in {subject}.
        - Submit your answers in a well-organized and polished format that showcases your qualifications and suitability for the role within {subject} at the Ampersand Group.
        - Provide the answer only without any additional information.
        - Do not include any index numbers or bullet points in your response.
    """

def grammer_prompt(txt: str, subject: str):
    return f"Rate the grammar score of the following speech on scale of 0-10. YOU WILL ONLY RETURN A INTEGER, WHICH IS THE SCORE. NOTHING ELSE. Speech: {txt}."
