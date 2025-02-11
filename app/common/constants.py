def knowledge_prompt(txt: str, subject: str, role: str, gen_answer: str):
    
    prompt = f"""The candidate has applied as for {role} as a {subject} position for a non-acedamic staff.
                    You are an expert evaluator assessing interview responses for a role in {subject}. Your 
                    task is to compare an AI-generated model answer with the candidate’s answer and assign 
                    scores based on predefined criteria. The evaluation should consider accuracy, clarity, 
                    relevance, depth, and overall effectiveness of the response.

                    The candidate's response:
                    {txt}
                    
                    The AI-generated model answer:
                    {gen_answer}

                    **Scoring Breakdown & Explanation**
                    Each score is rated on a 0 to 10 scale, where:
                    - 0-3 (Poor): Incomplete, off-topic, or lacks coherence.
                    - 4-6 (Average): Somewhat relevant but lacks depth, clarity, or structure.
                    - 7-8 (Good): Well-structured, relevant, and clear with minor areas for improvement.
                    - 9-10 (Excellent): Exceptional response with strong examples, deep insights, and clarity.
                    
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
                    
                    4. Communication Score (0-10)
                    - Reviews clarity, articulation, structure, and engagement.
                    -Assesses whether the response is concise and professional.
                    
                    5. Feedback Handling Score (0-10)
                    - Measures openness to constructive criticism.
                    - Looks at how well the candidate applies feedback for improvement.
                    
                    6. Overall Score (0-10)
                    - A weighted average of all the above categories.
                    - Provides a final assessment of the candidate’s response quality.

                    Generate a JSON output in the following format:                        
                    {{
                        "knowledge_score": [0-10],          # Evaluation of the introduction, clarity, and engagement.  
                        "introduction_score": [0-10],       # Assessment of industry knowledge, technical depth, and relevance.
                        "adaptability_score": [0-10],       # How well the candidate demonstrates flexibility and learning ability.
                        "communication_score": [0-10],      # Effectiveness in structuring and articulating thoughts.
                        "feedback_handling_score": [0-10],  # Assessment of how the candidate receives and applies feedback.
                        "overall_score": [0-10],            # Overall evaluation of the candidate's performance.
                        "detailed_feedback": {{
                            "introduction": ["Feedback on the introduction, clarity, and engagement."],
                            "knowledge": ["Feedback on industry knowledge, technical depth, and relevance."],
                            "adaptability": "How well the candidate demonstrates flexibility and learning ability.",
                            "communication": "Effectiveness in structuring and articulating thoughts.",
                            "feedback_handling": "Assessment of how the candidate receives and applies feedback."
                        }}
                    }}
                
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
        
        4. Why did you leave your last job?

        - Provide a professional and positive reason for leaving your previous role related to {subject}.
        - Avoid negativity about past employers and focus on career growth, new challenges, or alignment with career goals in {subject}.
        
        5. How do you prioritize tasks when handling multiple projects?

        - Describe your approach to prioritization in {subject}, such as using frameworks like Eisenhower Matrix, Agile methodologies, or industry-specific strategies.
        - Provide an example of a time when you effectively managed multiple projects in {subject}.
        
        6. How do you stay organized and manage your workload?

        - Explain the tools, techniques, or strategies you use to stay organized in {subject}, such as task management apps, scheduling methods, or workflow automation.
        - Give an example of how your organizational skills have helped you meet deadlines and maintain efficiency in {subject}.
        
        7.How do you handle feedback?

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
