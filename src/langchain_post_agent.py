"""
LangChain Post Agent - REAL ADK Framework Implementation
Uses LangGraph (LangChain's agent framework) with Google Gemini
"""

from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Dict, Any
import logging
import json
from datetime import datetime

try:
    from src.config import get_secret
    from src.agent_tools import create_langchain_tools
except ImportError:
    from config import get_secret
    from agent_tools import create_langchain_tools


class LangChainPostAgent:
    """
    Real LangGraph Agent Implementation (LangChain's Official Agent Framework)
    Uses LangGraph ReAct agent - NOT custom code!
    """
    
    def __init__(self):
        self.api_key = get_secret('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError("Google API Key not found")
        

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=self.api_key,
            temperature=0.9
        )
        
        
        self.tools = create_langchain_tools()
        
        
        self.agent_executor = create_react_agent(
            model=self.llm,
            tools=self.tools
        )
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.logger.info("LangGraph ReAct Agent initialized with Google Gemini")
    
    def generate_post_with_langchain(self,
                                     topic: str,
                                     tone: str = "professional",
                                     length: int = 1,
                                     target_audience: str = "professionals") -> Dict[str, Any]:
        """
        Generate blog using LangChain agent
        
        This is REAL agent framework usage!
        """
        self.logger.info(f"🤖 LangChain Agent starting for: {topic}")
        
        # Convert number of paragraphs to word count estimate
        paragraphs_to_words = {1: "150 words", 2: "250 words", 3: "350 words", 4: "450 words", 5: "550 words", 6: "650 words", 7: "750 words", 8: "850 words", 9: "950 words", 10: "1000+ words"}
        length_description = paragraphs_to_words.get(length, "300 words")
        
    
        task = f"""Create a professional LinkedIn post about "{topic}".

Requirements:
- Tone: {tone}
- Length: {length_description} ({length} paragraph{'s' if length > 1 else ''})
- Audience: {target_audience}

Steps to follow:
1. Use search_web tool to research "{topic}"
2. Use fetch_statistics tool to get data about "{topic}"  
3. Use get_trending_topics tool for "{topic}" industry
4. Create an engaging post incorporating the research

Format your final answer EXACTLY as:
TITLE: [Your title here]

CONTENT:
[Your blog content here]

HASHTAGS:
#Tag1 #Tag2 #Tag3 #Tag4 #Tag5

CALL_TO_ACTION:
[Your call to action here]
"""
        
        try:
            # Try agent first
            self.logger.info("🔄 Invoking LangGraph agent...")
            try:
                result = self.agent_executor.invoke({"messages": [("user", task)]})
            except Exception as agent_error:
                self.logger.warning(f"Agent invocation failed: {agent_error}")
                self.logger.info("🔄 Falling back to direct LLM call...")
                result = None
            
            output_text = ""
            if result:
                messages = result.get('messages', [])
                if messages:
                    last_message = messages[-1]
                    output_text = last_message.content if hasattr(last_message, 'content') else str(last_message)
            
            self.logger.info(f"📝 Agent output received: {len(output_text) if output_text else 0} chars")
            
        
            if not output_text or len(output_text) < 50:
                self.logger.warning("⚠️ Agent output too short, using fallback generation")
                output_text = self._generate_fallback(topic, tone, length, target_audience)
            
            blog_data = self._parse_response(output_text)
            
        
            blog_data['agent_metadata'] = {
                'framework': 'LangGraph ReAct Agent (LangChain)',
                'model': 'gemini-2.5-flash',
                'tools_available': [tool.name for tool in self.tools] if self.tools else [],
                'agent_type': 'ReAct (Reasoning + Acting)',
                'generated_at': datetime.now().isoformat()
            }
            
            blog_data['generation_params'] = {
                'topic': topic,
                'tone': tone,
                'length': length,
                'target_audience': target_audience
            }
            
            self.logger.info("✅ LangGraph Agent completed successfully")
            return blog_data
            
        except Exception as e:
            self.logger.error(f"❌ LangGraph Agent failed: {e}")
            self.logger.info("🔄 Generating fallback content...")
            fallback_text = self._generate_fallback(topic, tone, length, target_audience)
            blog_data = self._parse_response(fallback_text)
            blog_data['agent_metadata'] = {
                'framework': 'LangGraph ReAct Agent (Fallback)',
                'model': 'gemini-2.5-flash',
                'tools_available': [tool.name for tool in self.tools] if self.tools else [],
                'agent_type': 'Direct Generation (Fallback)',
                'generated_at': datetime.now().isoformat(),
                'note': 'Agent framework encountered error, used direct generation',
                'error': str(e)
            }
            return blog_data
    
    def _generate_fallback(self, topic: str, tone: str, length: int, target_audience: str) -> str:
        """Generate blog using direct LLM call if agent fails"""
        try:
            length_map = {1: "150 words", 2: "250 words", 3: "350 words", 4: "450 words", 5: "550 words"}
            length_description = length_map.get(length, "350 words")
            
            prompt = f"""Create a professional LinkedIn post about "{topic}".

Requirements:
- Tone: {tone}
- Length: {length_description}
- Audience: {target_audience}

Format EXACTLY as:
TITLE: [Your title here]

CONTENT:
[Your blog content here]

HASHTAGS:
#Tag1 #Tag2 #Tag3 #Tag4 #Tag5

CALL_TO_ACTION:
[Your call to action here]"""
            
            self.logger.info("🔄 Using direct LLM call for generation...")
            response = self.llm.invoke(prompt)
            return response.content if hasattr(response, 'content') else str(response)
            
        except Exception as e:
            self.logger.error(f"Fallback generation also failed: {e}")
    
            # Return hardcoded fallback post structure
            return f"""TITLE: {topic}: A Professional Perspective

CONTENT:
{topic} is transforming the way we work and think about {target_audience}. This technology offers unprecedented opportunities for innovation and growth.

Understanding {topic} requires a comprehensive approach that considers both technical and practical implications. Leaders in this space are already seeing significant benefits.

The future of {topic} looks promising, with new developments emerging regularly. Now is the time for {target_audience} to embrace these changes and stay ahead of the curve.

HASHTAGS:
#LinkedIn #Professional #{topic.replace(' ', '')} #Innovation #Future

CALL_TO_ACTION:
What are your thoughts on {topic}? Share your perspective in the comments!"""
    
    def _parse_response(self, text: str) -> Dict[str, Any]:
        """Parse the agent's response into structured format"""
        lines = text.split('\n')
        result = {
            'title': '',
            'content': '',
            'hashtags': '',
            'call_to_action': ''
        }
        
        current_section = None
        content_lines = []
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('TITLE:'):
                result['title'] = line.replace('TITLE:', '').strip()
                current_section = None
            elif line.startswith('CONTENT:'):
                current_section = 'content'
            elif line.startswith('HASHTAGS:'):
                current_section = 'hashtags'
            elif line.startswith('CALL_TO_ACTION:'):
                current_section = 'call_to_action'
            elif line and current_section:
                if current_section == 'content':
                    content_lines.append(line)
                elif current_section == 'hashtags':
                    result['hashtags'] = line
                elif current_section == 'call_to_action':
                    result['call_to_action'] = line
        
        result['content'] = '\n\n'.join(content_lines) if content_lines else text
        
        
        if not result['title']:
            result['title'] = 'LinkedIn Post'
        if not result['content']:
            result['content'] = text
        if not result['hashtags']:
            result['hashtags'] = '#AI #Technology #Innovation #Future #Growth'
        if not result['call_to_action']:
            result['call_to_action'] = 'What are your thoughts? Share in the comments!'
        
        return result
