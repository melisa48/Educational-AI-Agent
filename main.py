import random
from typing import Dict, List, Optional, Set, Tuple
from datetime import datetime

class EducationalAIAgent:
    def __init__(self):
        self.student_profiles = {}
        self.question_bank = {
            'math': {
                'easy': [
                    {'question': 'What is 5 + 7?', 'answer': 12, 'explanation': 'Adding 5 and 7 equals 12'},
                    {'question': 'What is 10 - 3?', 'answer': 7, 'explanation': 'Subtracting 3 from 10 equals 7'}
                ],
                'medium': [
                    {'question': 'What is 15 × 4?', 'answer': 60, 'explanation': 'Multiplying 15 by 4 equals 60'},
                    {'question': 'What is 72 ÷ 8?', 'answer': 9, 'explanation': 'Dividing 72 by 8 equals 9'}
                ],
                'hard': [
                    {'question': 'What is the square root of 144?', 'answer': 12, 'explanation': '12 × 12 = 144'},
                    {'question': 'What is 3² + 4²?', 'answer': 25, 'explanation': '3² (9) + 4² (16) = 25'}
                ]
            },
            'physics': {
                'easy': [
                    {'question': 'What is the SI unit of force?', 'answer': 'Newton', 'explanation': 'Force is measured in Newtons (N)'},
                    {'question': 'What does the formula F = ma represent?', 'answer': "Newton's Second Law", 'explanation': 'F = ma is Newton\'s Second Law of Motion'}
                ],
                'medium': [
                    {'question': 'Calculate the velocity of an object that traveled 50 meters in 10 seconds', 'answer': 5, 'explanation': 'Velocity = distance/time = 50m/10s = 5 m/s'},
                    {'question': 'What is the gravitational acceleration on Earth?', 'answer': 9.8, 'explanation': 'Gravitational acceleration on Earth is approximately 9.8 m/s²'}
                ],
                'hard': [
                    {'question': 'Calculate the kinetic energy of a 2kg object moving at 5 m/s', 'answer': 25, 'explanation': 'KE = 0.5 × mass × velocity² = 0.5 × 2 × 5² = 25 Joules'},
                    {'question': 'If work done is 100J and distance is 20m, what is the force applied?', 'answer': 5, 'explanation': 'Work = Force × Distance, so Force = Work/Distance = 100J/20m = 5N'}
                ]
            },
            'chemistry': {
                'easy': [
                    {'question': 'What is the chemical symbol for water?', 'answer': 'H2O', 'explanation': 'Water is composed of 2 hydrogen atoms and 1 oxygen atom'},
                    {'question': 'What is the atomic number of oxygen?', 'answer': 8, 'explanation': 'Oxygen has 8 protons in its nucleus'}
                ],
                'medium': [
                    {'question': 'What is the pH of pure water at 25°C?', 'answer': 7, 'explanation': 'Pure water has a neutral pH of 7'},
                    {'question': 'What gas is produced when an acid reacts with a carbonate?', 'answer': 'Carbon dioxide', 'explanation': 'Acid + Carbonate → Salt + Water + Carbon Dioxide'}
                ],
                'hard': [
                    {'question': 'Balance this equation: __ Fe + __ O2 → __ Fe2O3', 'answer': '4 Fe + 3 O2 → 2 Fe2O3', 'explanation': 'Balanced equation requires 4 iron atoms and 3 oxygen molecules'},
                    {'question': 'Calculate the molarity of a solution with 4 moles of solute in 2 liters of solution', 'answer': 2, 'explanation': 'Molarity = moles of solute/volume of solution in liters = 4 moles/2 L = 2 M'}
                ]
            }
        }

    def create_student_profile(self, student_id: str, name: str) -> None:
        """Create a new student profile with initial settings."""
        subjects = list(self.question_bank.keys())
        self.student_profiles[student_id] = {
            'name': name,
            'performance_history': [],
            'current_level': {subject: 'easy' for subject in subjects},
            'topics_mastered': set(),
            'learning_style': None,
            'preferred_topics': set(),
            'quiz_attempts': [],
            'last_activity': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def assess_learning_style(self, student_id: str, quiz_responses: List[Dict]) -> str:
        """
        Analyze quiz responses to determine learning style.
        Returns: 'visual', 'auditory', or 'kinesthetic'
        """
        # Simplified learning style assessment
        styles = {'visual': 0, 'auditory': 0, 'kinesthetic': 0}
        
        for response in quiz_responses:
            if response.get('preference') == 'diagrams':
                styles['visual'] += 1
            elif response.get('preference') == 'verbal_explanation':
                styles['auditory'] += 1
            elif response.get('preference') == 'hands_on':
                styles['kinesthetic'] += 1

        learning_style = max(styles, key=styles.get)
        self.student_profiles[student_id]['learning_style'] = learning_style
        self.student_profiles[student_id]['last_activity'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return learning_style

    def generate_quiz(self, student_id: str, subject: str) -> List[Dict]:
        """Generate a quiz based on student's current level."""
        current_level = self.student_profiles[student_id]['current_level'][subject]
        available_questions = self.question_bank[subject][current_level]
        self.student_profiles[student_id]['last_activity'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return random.sample(available_questions, min(3, len(available_questions)))

    def evaluate_quiz(self, student_id: str, subject: str, student_answers: List) -> Dict:
        """
        Evaluate quiz responses and provide feedback.
        Returns performance metrics and personalized feedback.
        """
        profile = self.student_profiles[student_id]
        current_level = profile['current_level'][subject]
        
        # Generate a quiz and capture it for later reference
        quiz = self.generate_quiz(student_id, subject)
        correct_count = 0
        feedback = []
        detailed_responses = []
        
        for i, (question, answer) in enumerate(zip(quiz, student_answers)):
            is_correct = self._check_answer(question, answer)
            if is_correct:
                correct_count += 1
                feedback.append(f"Question {i+1}: Correct!")
            else:
                feedback.append(f"Question {i+1}: Incorrect. {question['explanation']}")
            
            # Track detailed responses
            detailed_responses.append({
                'question': question['question'],
                'student_answer': answer,
                'correct_answer': question['answer'],
                'is_correct': is_correct,
                'explanation': question['explanation']
            })

        score = (correct_count / len(student_answers)) * 100
        
        # Update student's level based on performance
        old_level = current_level
        if score >= 80 and current_level == 'easy':
            profile['current_level'][subject] = 'medium'
        elif score >= 80 and current_level == 'medium':
            profile['current_level'][subject] = 'hard'
        elif score <= 30 and current_level != 'easy':
            profile['current_level'][subject] = 'easy'
        
        # Check if the topic is mastered (completed hard level with high score)
        if score >= 80 and current_level == 'hard':
            profile['topics_mastered'].add(subject)
        
        # Record quiz attempt
        profile['quiz_attempts'].append({
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'subject': subject,
            'level': current_level,
            'score': score,
            'questions': quiz,
            'student_answers': student_answers,
            'detailed_responses': detailed_responses
        })
        
        profile['performance_history'].append({
            'subject': subject,
            'score': score,
            'level': current_level,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        profile['last_activity'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return {
            'score': score,
            'feedback': feedback,
            'previous_level': old_level,
            'new_level': profile['current_level'][subject],
            'detailed_responses': detailed_responses,
            'recommendations': self.generate_recommendations(student_id, subject, score),
            'mastered': subject in profile['topics_mastered']
        }

    def _check_answer(self, question: Dict, student_answer) -> bool:
        """Helper method to check if an answer is correct, with type flexibility."""
        # If the expected answer is a string and the student answer is a string, do case-insensitive comparison
        if isinstance(question['answer'], str) and isinstance(student_answer, str):
            return student_answer.lower() == question['answer'].lower()
        # Otherwise do direct comparison (for numbers, etc.)
        return student_answer == question['answer']

    def generate_recommendations(self, student_id: str, subject: str, score: float) -> List[str]:
        """Generate personalized learning recommendations based on performance."""
        profile = self.student_profiles[student_id]
        recommendations = []

        if score < 60:
            recommendations.append(f"Review the basics of {subject} before proceeding.")
            if profile['learning_style'] == 'visual':
                recommendations.append("Try using diagrams and visual aids to understand the concepts better.")
            elif profile['learning_style'] == 'auditory':
                recommendations.append("Consider watching video explanations or using verbal reasoning.")
            else:  # kinesthetic
                recommendations.append("Practice with hands-on exercises and interactive problems.")

        elif score >= 60 and score < 80:
            recommendations.append("You're doing well! Practice more to master these concepts.")
            recommendations.append("Try solving similar problems with different variations.")

        else:
            recommendations.append("Excellent work! You're ready for more challenging problems.")
            if profile['current_level'][subject] != 'hard':
                recommendations.append("Consider moving to the next difficulty level.")
            else:
                recommendations.append(f"You've mastered the {subject} content at this level!")

        return recommendations

    def provide_explanation(self, topic: str, concept: str, student_id: str) -> str:
        """
        Provide personalized explanations based on the student's learning style.
        """
        learning_style = self.student_profiles[student_id]['learning_style']
        self.student_profiles[student_id]['last_activity'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        explanations = {
            'visual': f"Here's a visual representation of {concept} in {topic}...",
            'auditory': f"Let me explain {concept} in {topic} step by step...",
            'kinesthetic': f"Let's work through {concept} in {topic} with some hands-on examples..."
        }
        
        return explanations.get(learning_style, "Here's a general explanation...")

    def track_progress(self, student_id: str) -> Dict:
        """Generate a progress report for the student."""
        profile = self.student_profiles[student_id]
        self.student_profiles[student_id]['last_activity'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return {
            'name': profile['name'],
            'learning_style': profile['learning_style'],
            'current_levels': profile['current_level'],
            'topics_mastered': list(profile['topics_mastered']),
            'total_quizzes_taken': len(profile['quiz_attempts']),
            'average_scores': self._calculate_average_scores(profile),
            'performance_trend': self._calculate_performance_trend(profile['performance_history']),
            'last_activity': profile['last_activity'],
            'recommendations': self._generate_progress_recommendations(profile)
        }

    def _calculate_average_scores(self, profile: Dict) -> Dict:
        """Calculate average scores per subject."""
        if not profile['performance_history']:
            return {}
        
        scores_by_subject = {}
        for entry in profile['performance_history']:
            subject = entry['subject']
            if subject not in scores_by_subject:
                scores_by_subject[subject] = []
            scores_by_subject[subject].append(entry['score'])
        
        return {subject: sum(scores)/len(scores) for subject, scores in scores_by_subject.items()}

    def _calculate_performance_trend(self, history: List[Dict]) -> Dict:
        if not history:
            return {"overall": "Not enough data"}
        
        # Group history by subject
        history_by_subject = {}
        for entry in history:
            subject = entry['subject']
            if subject not in history_by_subject:
                history_by_subject[subject] = []
            history_by_subject[subject].append(entry)
        
        trends = {}
        for subject, entries in history_by_subject.items():
            if len(entries) < 3:
                trends[subject] = "Collecting data"
                continue
                
            recent_scores = [entry['score'] for entry in entries[-3:]]
            avg_change = (recent_scores[-1] - recent_scores[0]) / len(recent_scores)
            
            if avg_change > 5:
                trends[subject] = "Improving"
            elif avg_change < -5:
                trends[subject] = "Needs attention"
            else:
                trends[subject] = "Stable"
        
        # Add overall trend
        if len(trends) > 0:
            improving_count = sum(1 for trend in trends.values() if trend == "Improving")
            needs_attention_count = sum(1 for trend in trends.values() if trend == "Needs attention")
            
            if improving_count > needs_attention_count:
                trends["overall"] = "Improving"
            elif needs_attention_count > improving_count:
                trends["overall"] = "Needs attention"
            else:
                trends["overall"] = "Stable"
        else:
            trends["overall"] = "Not enough data"
        
        return trends

    def _generate_progress_recommendations(self, profile: Dict) -> List[str]:
        """Generate overall progress recommendations."""
        recommendations = []
        
        # Look at mastered topics
        if profile['topics_mastered']:
            mastered_list = ", ".join(list(profile['topics_mastered']))
            recommendations.append(f"Congratulations! You've mastered: {mastered_list}")
        
        # Analyze performance history by subject
        if profile['performance_history']:
            subject_scores = {}
            for entry in profile['performance_history']:
                subject = entry['subject']
                if subject not in subject_scores:
                    subject_scores[subject] = []
                subject_scores[subject].append(entry['score'])
            
            # Find subjects that need attention or are excelling
            for subject, scores in subject_scores.items():
                avg_score = sum(scores) / len(scores)
                if avg_score < 60:
                    recommendations.append(f"Consider focusing more on {subject}, your average score is {avg_score:.1f}%")
                elif avg_score > 80:
                    recommendations.append(f"You're excelling in {subject} with an average of {avg_score:.1f}%")
        
        # Encourage mastery
        if not profile['topics_mastered']:
            recommendations.append("Focus on mastering at least one topic to build confidence")
        
        # Encourage utilizing learning style
        if profile['learning_style'] == 'visual':
            recommendations.append("Continue utilizing your visual learning style")
        elif profile['learning_style'] == 'auditory':
            recommendations.append("Continue utilizing your auditory learning style")
        elif profile['learning_style'] == 'kinesthetic':
            recommendations.append("Continue utilizing your kinesthetic learning style")
        
        return recommendations
# Example Usage:
agent = EducationalAIAgent()

# Create student profiles
agent.create_student_profile('john_doe', 'John Doe')
agent.create_student_profile('jane_smith', 'Jane Smith')
agent.create_student_profile('alex_johnson', 'Alex Johnson')

# John Doe's interactions
print("Generated math quiz for John Doe:")
quiz_john_math = agent.generate_quiz('john_doe', 'math')
for i, question in enumerate(quiz_john_math):
    print(f"Question {i+1}: {question['question']}")
student_answers_john_math = [12, 7]
print("Student answers:", student_answers_john_math)
quiz_results_john_math = agent.evaluate_quiz('john_doe', 'math', student_answers_john_math)
print("Quiz Results:")
print(f"Score: {quiz_results_john_math['score']}%")
print("Feedback:")
for feedback in quiz_results_john_math['feedback']:
    print(f"  {feedback}")
print("Detailed responses:")
for response in quiz_results_john_math['detailed_responses']:
    print(f"  Question: {response['question']}")
    print(f"    Student answer: {response['student_answer']}")
    print(f"    Correct answer: {response['correct_answer']}")
    print(f"    Correct: {'Yes' if response['is_correct'] else 'No'}")
print(f"Level change: {quiz_results_john_math['previous_level']} → {quiz_results_john_math['new_level']}")
print("Recommendations:")
for recommendation in quiz_results_john_math['recommendations']:
    print(f"  {recommendation}")

print("\nGenerated chemistry quiz for John Doe:")
quiz_john_chem = agent.generate_quiz('john_doe', 'chemistry')
for i, question in enumerate(quiz_john_chem):
    print(f"Question {i+1}: {question['question']}")
student_answers_john_chem = ['H2O', 7]
print("Student answers:", student_answers_john_chem)
quiz_results_john_chem = agent.evaluate_quiz('john_doe', 'chemistry', student_answers_john_chem)
print("Quiz Results:")
print(f"Score: {quiz_results_john_chem['score']}%")
print("Feedback:")
for feedback in quiz_results_john_chem['feedback']:
    print(f"  {feedback}")
print("Detailed responses:")
for response in quiz_results_john_chem['detailed_responses']:
    print(f"  Question: {response['question']}")
    print(f"    Student answer: {response['student_answer']}")
    print(f"    Correct answer: {response['correct_answer']}")
    print(f"    Correct: {'Yes' if response['is_correct'] else 'No'}")
print(f"Level change: {quiz_results_john_chem['previous_level']} → {quiz_results_john_chem['new_level']}")
print("Recommendations:")
for recommendation in quiz_results_john_chem['recommendations']:
    print(f"  {recommendation}")

# Jane Smith's interactions
print("\nGenerated physics quiz for Jane Smith:")
quiz_jane_physics = agent.generate_quiz('jane_smith', 'physics')
for i, question in enumerate(quiz_jane_physics):
    print(f"Question {i+1}: {question['question']}")
student_answers_jane_physics = ['Wrong answer', 'Newton']
print("Student answers:", student_answers_jane_physics)
quiz_results_jane_physics = agent.evaluate_quiz('jane_smith', 'physics', student_answers_jane_physics)
print("Quiz Results:")
print(f"Score: {quiz_results_jane_physics['score']}%")
print("Feedback:")
for feedback in quiz_results_jane_physics['feedback']:
    print(f"  {feedback}")
print("Detailed responses:")
for response in quiz_results_jane_physics['detailed_responses']:
    print(f"  Question: {response['question']}")
    print(f"    Student answer: {response['student_answer']}")
    print(f"    Correct answer: {response['correct_answer']}")
    print(f"    Correct: {'Yes' if response['is_correct'] else 'No'}")
print(f"Level change: {quiz_results_jane_physics['previous_level']} → {quiz_results_jane_physics['new_level']}")
print("Recommendations:")
for recommendation in quiz_results_jane_physics['recommendations']:
    print(f"  {recommendation}")

# Alex Johnson's interactions: assessing learning style with a quiz
print("\nAssessing learning style for Alex Johnson:")
learning_style_quiz_responses = [
    {'preference': 'hands_on'},
    {'preference': 'verbal_explanation'},
    {'preference': 'hands_on'}
]
learning_style = agent.assess_learning_style('alex_johnson', learning_style_quiz_responses)
print(f"Learning Style: {learning_style}")

#Progress Reports
print("\nProgress Report for John Doe:")
progress_report_john = agent.track_progress('john_doe')
print(f"Learning Style: {progress_report_john['learning_style']}")
print(f"Current Levels: {progress_report_john['current_levels']}")
print(f"Topics Mastered: {progress_report_john['topics_mastered']}")
print(f"Total Quizzes Taken: {progress_report_john['total_quizzes_taken']}")
if progress_report_john['average_scores']:
    print("Average Scores by Subject:")
    for subject, score in progress_report_john['average_scores'].items():
        print(f"  {subject}: {score:.1f}%")
print(f"Performance Trends: {progress_report_john['performance_trend']}")
print("Overall Recommendations:")
for recommendation in progress_report_john['recommendations']:
    print(f"  {recommendation}")

print("\nProgress Report for Jane Smith:")
progress_report_jane = agent.track_progress('jane_smith')
print(f"Learning Style: {progress_report_jane['learning_style']}")
print(f"Current Levels: {progress_report_jane['current_levels']}")
print(f"Topics Mastered: {progress_report_jane['topics_mastered']}")
print(f"Total Quizzes Taken: {progress_report_jane['total_quizzes_taken']}")
if progress_report_jane['average_scores']:
    print("Average Scores by Subject:")
    for subject, score in progress_report_jane['average_scores'].items():
        print(f"  {subject}: {score:.1f}%")
print(f"Performance Trends: {progress_report_jane['performance_trend']}")
print("Overall Recommendations:")
for recommendation in progress_report_jane['recommendations']:
    print(f"  {recommendation}")

print("\nProgress Report for Alex Johnson:")
progress_report_alex = agent.track_progress('alex_johnson')
print(f"Learning Style: {progress_report_alex['learning_style']}")
print(f"Current Levels: {progress_report_alex['current_levels']}")
print(f"Topics Mastered: {progress_report_alex['topics_mastered']}")
print(f"Total Quizzes Taken: {progress_report_alex['total_quizzes_taken']}")
if progress_report_alex['average_scores']:
    print("Average Scores by Subject:")
    for subject, score in progress_report_alex['average_scores'].items():
        print(f"  {subject}: {score:.1f}%")
print(f"Performance Trends: {progress_report_alex['performance_trend']}")
print("Overall Recommendations:")
for recommendation in progress_report_alex['recommendations']:
    print(f"  {recommendation}")
