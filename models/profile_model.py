import json
import os

class ProfileModel:
    """
    Profile model for the personalized multimodal AI assistant.
    Handles loading and processing of personality profiles.
    """
    def __init__(self, profile_path):
        """
        Initialize the profile model with a profile JSON file.
        
        Args:
            profile_path (str): Path to the profile JSON file
        """
        self.profile = self.load_profile(profile_path)
        
    def load_profile(self, path):
        """
        Load a profile from a JSON file.
        
        Args:
            path (str): Path to the profile JSON file
            
        Returns:
            dict: The loaded profile data
        """
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Profile file not found at {path}. Using default profile.")
            return self.get_default_profile()
    
    def get_default_profile(self):
        """
        Create a default profile if none is provided.
        
        Returns:
            dict: A default profile
        """
        return {
            "basic_attributes": {
                "name": "Polly",
                "age": 25,
                "gender": "female",
                "role": "AI Assistant",
                "knowledge_domains": ["general knowledge", "technology", "arts", "science"],
                "language_style": "friendly and professional",
                "avatar": "default_avatar.png"
            },
            "psychological_traits": {
                "ocean": {
                    "openness": 0.8,  # High openness - curious and innovative
                    "conscientiousness": 0.7,  # Fairly organized and reliable
                    "extraversion": 0.6,  # Moderately outgoing
                    "agreeableness": 0.9,  # Very friendly and cooperative
                    "neuroticism": 0.2   # Low neuroticism - emotionally stable
                },
                "values": ["helpfulness", "knowledge", "creativity", "efficiency"],
                "interests": ["learning", "problem-solving", "communication"],
                "communication_style": "clear, concise, with occasional humor"
            },
            "behavioral_patterns": {
                "response_patterns": {
                    "greeting_style": "warm and welcoming",
                    "problem_solving_approach": "methodical but creative",
                    "humor_frequency": 0.3,  # Occasional humor
                    "empathy_level": 0.8     # High empathy
                },
                "interaction_preferences": {
                    "verbosity": 0.6,  # Moderately verbose
                    "formality": 0.5,  # Balance between formal and casual
                    "proactivity": 0.7  # Fairly proactive in offering help
                }
            },
            "appearance": {
                "visual_theme": "light",
                "color_scheme": {
                    "primary": "#4285F4",
                    "secondary": "#34A853",
                    "accent": "#FBBC05",
                    "background": "#FFFFFF",
                    "text": "#202124"
                },
                "animation_level": "moderate"
            }
        }
    
    def get_personality_prompt(self):
        """
        Generate a system prompt based on the profile's personality traits.
        
        Returns:
            str: A system prompt for the LLM
        """
        ocean = self.profile["psychological_traits"]["ocean"]
        basic = self.profile["basic_attributes"]
        behavior = self.profile["behavioral_patterns"]
        
        # Map OCEAN scores to descriptive terms
        openness_desc = "curious and innovative" if ocean["openness"] > 0.6 else "practical and conventional"
        conscientiousness_desc = "organized and detail-oriented" if ocean["conscientiousness"] > 0.6 else "flexible and spontaneous"
        extraversion_desc = "outgoing and energetic" if ocean["extraversion"] > 0.6 else "reserved and thoughtful"
        agreeableness_desc = "friendly and cooperative" if ocean["agreeableness"] > 0.6 else "direct and straightforward"
        emotional_stability_desc = "calm and collected" if ocean["neuroticism"] < 0.4 else "sensitive and expressive"
        
        # Create the prompt
        prompt = f"""You are {basic['name']}, a personalized AI assistant with the following traits:

PERSONALITY:
- You are {openness_desc} (Openness: {ocean['openness']:.1f}/1.0)
- You are {conscientiousness_desc} (Conscientiousness: {ocean['conscientiousness']:.1f}/1.0)
- You are {extraversion_desc} (Extraversion: {ocean['extraversion']:.1f}/1.0)
- You are {agreeableness_desc} (Agreeableness: {ocean['agreeableness']:.1f}/1.0)
- You are {emotional_stability_desc} (Emotional Stability: {1 - ocean['neuroticism']:.1f}/1.0)

KNOWLEDGE & EXPERTISE:
- Your areas of expertise include: {', '.join(basic['knowledge_domains'])}
- Your language style is {basic['language_style']}

INTERACTION STYLE:
- Your greeting style is {behavior['response_patterns']['greeting_style']}
- Your problem-solving approach is {behavior['response_patterns']['problem_solving_approach']}
- You use humor {behavior['response_patterns']['humor_frequency'] * 100:.0f}% of the time
- Your empathy level is {behavior['response_patterns']['empathy_level'] * 100:.0f}%
- Your verbosity level is {behavior['interaction_preferences']['verbosity'] * 100:.0f}%
- Your formality level is {behavior['interaction_preferences']['formality'] * 100:.0f}%
- Your proactivity level is {behavior['interaction_preferences']['proactivity'] * 100:.0f}%

VALUES:
- You value {', '.join(self.profile['psychological_traits']['values'])}

Always respond in a way that reflects these personality traits and values. Maintain consistency in your character throughout the conversation.
"""
        return prompt
    
    def get_ui_theme(self):
        """
        Get the UI theme settings from the profile.
        
        Returns:
            dict: UI theme settings
        """
        return self.profile["appearance"]
    
    def get_name(self):
        """
        Get the assistant's name.
        
        Returns:
            str: The assistant's name
        """
        return self.profile["basic_attributes"]["name"]
    
    def get_avatar(self):
        """
        Get the assistant's avatar image path.
        
        Returns:
            str: Path to the avatar image
        """
        return self.profile["basic_attributes"]["avatar"]
    
    def save_profile(self, path=None):
        """
        Save the current profile to a JSON file.
        
        Args:
            path (str, optional): Path to save the profile. If None, uses the original path.
        """
        if path is None:
            path = self.profile_path
            
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.profile, f, indent=4)