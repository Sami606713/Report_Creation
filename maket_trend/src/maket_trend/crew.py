from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# Uncomment the following line to use an example of a custom tool
from maket_trend.tools.custom_tool import MarketReport
from langchain_groq import ChatGroq
import os

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

def load_llm():
	llm=ChatGroq(api_key=os.getenv("GROQ_API_KEY"),model="mixtral-8x7b-32768")
	return llm

@CrewBase
class MaketTrendCrew():
	"""ReportGeneration crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def market_researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['market_researcher'],
			tools=[MarketReport.get_content], # Example of custom tool, loaded on the beginning of file
			verbose=True,
			llm=load_llm(),
			allow_delegation=True
		)


	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
			output_file='report_generation/market_research.txt'
		)

	@agent
	def research_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['research_writer'],
			tools=[MarketReport.get_content], # Example of custom tool, loaded on the beginning of file
			verbose=True,
			llm=load_llm(),
			allow_delegation=True
		)


	@task
	def writing_task(self) -> Task:
		return Task(
			config=self.tasks_config['writing_task'],
			output_file='report_generation/final_report.txt'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the MarketReportGeneration crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)