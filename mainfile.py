from langchain_anthropic import ChatAnthropic
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
import subprocess
import os
import requests
class NewsCollector:
    def __init__(self, newsapi_key):
        self.newsapi_key = newsapi_key
    
    def get_news(self, keywords="economy", language="en"):
        """get news"""
        base_url = "https://newsapi.org/v2/everything"
        
        params = {
            "q": keywords,
            "language": language,
            "sortBy": "publishedAt",
            "pageSize": 5,
            "apiKey": self.newsapi_key
        }
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            news = response.json()
            
            if news["status"] == "ok" and news["articles"]:
                article = news["articles"][0]
                return {
                    "title": article["title"],
                    "content": article["description"],
                    "url": article["url"]
                }
            
        except Exception as e:
            print(f"get news error：{str(e)}")
        return None
   

class ManimAutomation:
    def __init__(self, anthropic_api_key, newsapi_key):
        self.llm = ChatAnthropic(
            model="claude-3-sonnet-20240229",  # 更新模型名称
            anthropic_api_key=anthropic_api_key,  # 明确传入 API key
            temperature=0.7
        )
        
        self.news_collector = NewsCollector(newsapi_key)
        
        self.manim_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a professional Manim animation expert.
            Please generate engaging Manim animation code based on the provided news content.
            The code should include:
            1. Required Manim imports
            2. Clear scene class definition (use NewsVisualizationScene as class name)
            3. High-quality settings (1080p/60fps)
            4. Rich visual elements (text effects, shapes, transitions)
            5. Professional animations and timing
            6. Minimum 30-second duration
            7. Do not output any text except the code
            
            Example structure (do not copy directly):
            ```python
            from manim import *
            class NewsVisualizationScene(Scene):
                # Your animation code here
            ```
            """),
            ("human", "News content: {story}\nPlease generate corresponding Manim animation code."),
        ])
        
        self.chain = LLMChain(llm=self.llm, prompt=self.manim_prompt)
    
    def get_story(self):
        """get news and format to story"""
        news = self.news_collector.get_news()
        
        if news:
            story = f"""
            today news：{news['title']}
            
            content summary：{news['content']}
            
            news source：{news['url']}
            """
            return story, news['title']
        else:
            return """
            this is a story about the relationship between supply and demand in economics.
            when the price of a good rises, the supply increases and the demand decreases;
            when the price of a good falls, the supply decreases and the demand increases.
            in the end, the market reaches equilibrium.
            """, "supply and demand animation"
    def generate_manim_code(self, story):
        """generate manim code based on story"""
        try:
            manim_code = self.chain.invoke({"story": story})
            manim_code = self.output_code_parser(manim_code)
            # 將生成的代碼保存到文件
            #print(manim_code[manim_code.index("```python")+9:manim_code.rindex("```")])
            with open("generated_animation.py", "w", encoding="utf-8") as f:
                f.write(manim_code)
            #print(manim_code)
            print("success generate manim code!")
            return "generated_animation.py"
        except Exception as e:
            print(f"generate code error：{str(e)}")
            return None
    
    def render_animation(self, scene_name):
        """render manim animation"""
        try:
            # set command and environment variables
            command = f"manim -pqh generated_animation.py {scene_name}"
            env = {
                **os.environ,
                'PYTHONIOENCODING': 'utf-8',
                'PYTHONUTF8': '1'  # set python use utf-8
            }
            
            # use subprocess.Popen instead of subprocess.run
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                encoding='utf-8',  # set encoding to utf-8
                errors='ignore'    # ignore error
            )
            
            # read output
            stdout, stderr = process.communicate()
            
            if process.returncode == 0:
                print("animation render success!")
                return True
            else:
                print(f"render error：{stderr}")
                return False
                
        except Exception as e:
            print(f"render error：{str(e)}")
            return False
    
    def output_code_parser(self, code):
        """parse output code, handle multiple code block formats"""
        try:
            # handle standard ```python format
            if "```python" in code:
                return code[code.index("```python")+9:code.rindex("```")].strip()
            # handle normal ``` format
            elif "```" in code:
                return code[code.index("```")+3:code.rindex("```")].strip()
            # if no symbol, return original code
            return code.strip()
        except Exception as e:
            print(f"code parse error：{str(e)}")
            return code.strip()
def main():
    # initialize automation tool
    automation = ManimAutomation(
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
        newsapi_key=os.getenv("NEWSAPI_KEY")
    )
    
    # 1. get news story
    story, news_title = automation.get_story()
    print("get news：")
    print(story)
    
    # 2. generate manim code
    code_file = automation.generate_manim_code(story)
    if not code_file:
        return
    
    # 3. render animation
    if not automation.render_animation("NewsVisualizationScene"):
        return
    

if __name__ == "__main__":
    main()