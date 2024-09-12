# from crewai_tools import BaseTool
# class MyCustomTool(BaseTool):
#     name: str = "Name of my tool"
#     description: str = (
#         "Clear description for what this tool is useful for, you agent will need this information to use it."
#     )

#     def _run(self, argument: str) -> str:
#         # Implementation goes here
#         return "this is an example of a tool output, ignore it and move along."


from langchain_community.tools import TavilySearchResults
from langchain.tools import tool
from dotenv import load_dotenv
import getpass
import os
load_dotenv()

os.environ['tavily_api_key']

class MarketReport:
    @tool("search content")
    def get_content(query:str):
        """
        This tool can conduct the today market research and return the output of top 20 american companies.
        Date: 9 Sep 2022
        """
        tool = TavilySearchResults(
        max_results=20,
        search_depth="advanced",
        include_answer=True,
        include_raw_content=True,
        include_images=True
        )
        # Invoke the query
        response=tool.invoke(input = {"query":query})

        # print(response)
        final_output=""
        for i in range(len(response)):
            final_output+="**URL**: "+ response[i]["url"] +"\n"
            final_output+="**content**: "+ response[i]["content"] +"\n"
            
        return final_output

# if __name__=="__main__":
#     m=MarketReport()
#     response=m.get_content("automobile inductry")
#     print(response)