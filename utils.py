"""
UTILITY FUNCTIONS FOR LINKEDIN POST AGENT
Helper functions for post generation, email sending, and data management
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List


class PostManager:
    """Manage post generation and storage"""
    
    def __init__(self, history_file: str = "post_history.json"):
        self.history_file = history_file
        self.history = self.load_history()
    
    def load_history(self) -> List[Dict]:
        """Load post history from file"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_history(self):
        """Save post history to file"""
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def add_post(self, topic: str, content: str, params: Dict[str, Any]):
        """Add a post to history"""
        post = {
            'id': len(self.history) + 1,
            'topic': topic,
            'content': content,
            'params': params,
            'created_at': datetime.now().isoformat(),
        }
        self.history.append(post)
        self.save_history()
        return post
    
    def get_post(self, post_id: int) -> Dict:
        """Get a specific post"""
        for post in self.history:
            if post['id'] == post_id:
                return post
        return None
    
    def delete_post(self, post_id: int) -> bool:
        """Delete a post"""
        self.history = [p for p in self.history if p['id'] != post_id]
        self.save_history()
        return True
    
    def get_all_posts(self) -> List[Dict]:
        """Get all posts"""
        return self.history
    
    def get_posts_by_topic(self, topic: str) -> List[Dict]:
        """Get posts by topic"""
        return [p for p in self.history if topic.lower() in p['topic'].lower()]


class FormValidator:
    """Validate user inputs"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        return '@' in email and '.' in email.split('@')[1]
    
    @staticmethod
    def validate_topic(topic: str) -> bool:
        """Validate topic"""
        return len(topic.strip()) > 0 and len(topic.strip()) <= 500
    
    @staticmethod
    def validate_audience(audience: str) -> bool:
        """Validate audience"""
        return len(audience.strip()) > 0 and len(audience.strip()) <= 100


class PostFormatter:
    """Format post content"""
    
    @staticmethod
    def format_with_emojis(content: str) -> str:
        """Add emojis to content"""
        return content
    
    @staticmethod
    def format_as_markdown(content: str) -> str:
        """Format content as markdown"""
        lines = content.split('\n')
        formatted = []
        for line in lines:
            if line.strip():
                formatted.append(f"- {line.strip()}")
        return '\n'.join(formatted)
    
    @staticmethod
    def format_as_html(content: str) -> str:
        """Format content as HTML"""
        return f"<p>{content.replace(chr(10), '</p><p>')}</p>"


class Analytics:
    """Track analytics"""
    
    def __init__(self, analytics_file: str = "analytics.json"):
        self.analytics_file = analytics_file
        self.data = self.load_analytics()
    
    def load_analytics(self) -> Dict:
        """Load analytics data"""
        if os.path.exists(self.analytics_file):
            try:
                with open(self.analytics_file, 'r') as f:
                    return json.load(f)
            except:
                return self._default_analytics()
        return self._default_analytics()
    
    def _default_analytics(self) -> Dict:
        """Default analytics structure"""
        return {
            'total_posts': 0,
            'total_emails': 0,
            'total_api_calls': 0,
            'avg_generation_time': 0,
            'most_used_tone': {},
            'most_used_length': {},
            'last_updated': datetime.now().isoformat()
        }
    
    def save_analytics(self):
        """Save analytics"""
        with open(self.analytics_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def increment_posts(self):
        """Increment post count"""
        self.data['total_posts'] += 1
        self.data['last_updated'] = datetime.now().isoformat()
        self.save_analytics()
    
    def increment_emails(self):
        """Increment email count"""
        self.data['total_emails'] += 1
        self.data['last_updated'] = datetime.now().isoformat()
        self.save_analytics()


def get_tone_emoji(tone: str) -> str:
    """Get emoji for tone"""
    tone_emojis = {
        'professional': '💼',
        'motivational': '🚀',
        'personal': '👤',
        'educational': '📚'
    }
    return tone_emojis.get(tone.lower(), '💭')


def get_length_description(length: str) -> str:
    """Get description for length"""
    descriptions = {
        'short': '1-2 paragraphs',
        'medium': '3-4 paragraphs',
        'long': '5+ paragraphs'
    }
    return descriptions.get(length.lower(), 'Medium')


def format_timestamp(timestamp: str) -> str:
    """Format timestamp for display"""
    try:
        dt = datetime.fromisoformat(timestamp)
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return timestamp


def export_post_as_text(post: Dict) -> str:
    """Export post as plain text"""
    content = f"""
LINKEDIN POST
Generated: {post.get('created_at', 'Unknown')}
Topic: {post.get('topic', 'Unknown')}

---

{post.get('content', '')}

---
Generated by LinkedIn Post Agent 9000
"""
    return content.strip()


def export_post_as_json(post: Dict) -> str:
    """Export post as JSON"""
    return json.dumps(post, indent=2)
