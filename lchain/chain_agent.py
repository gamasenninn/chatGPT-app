from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from dotenv import load_dotenv

load_dotenv()

# First, let's load the language model we're going to use to control the agent.
chat = ChatOpenAI(temperature=0)

# Next, let's load some tools to use. Note that the `llm-math` tool uses an LLM, so we need to pass that in.
llm = OpenAI(temperature=0)
tools = load_tools(["wikipedia","python_repl","serpapi", "llm-math"], llm=llm)


# Finally, let's initialize an agent with the tools, the language model, and the type of agent we want to use.
agent = initialize_agent(tools, chat, agent="chat-zero-shot-react-description", verbose=True)

# Now let's test it out!


agent.run("pythonでフィボナッチ数を求める関数fibo()を作成し、fibo(10)を求めてください")


#agent.run("How much did Ryoma Sakamoto make in trade?")

#agent.run("what does marie ono's paper say in the world of fluid dynamics? Please elaborate.")

#agent.run("坂本龍馬は貿易でどのくらい売上たのですか？")
'''
agent.run(
First of all, please review the rules of Sudoku.
Then, Solve the x puzzle by python.
x=[
[4,0,9,1,8,0,0,0,0],
[1,7,0,5,0,0,0,3,0],
[0,3,0,0,0,0,0,0,8],
[0,0,0,4,0,2,0,0,0],
[0,9,0,0,0,0,2,4,0],
[2,0,3,0,0,0,0,0,5],
[0,1,0,0,0,0,0,0,3],
[3,0,7,0,0,1,8,0,9],
[0,0,0,0,9,7,1,6,0],
]

)
'''
def repl():

    while True:
        try:
            user_input = input(">")
            if user_input:
                agent.run(user_input)
                
        except (KeyboardInterrupt, EOFError):
            print()
            break

