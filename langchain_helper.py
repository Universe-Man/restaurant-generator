import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableSequence

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)


def generate_restaurant_name_and_items(cuisine):
    # Chain 1 : Restaurant Name
    prompt_template_name = PromptTemplate(
        input_variables=["cuisine"],
        template="I want to open a restaurant for {cuisine} food. Suggest a fancy name for this.",
    )

    name_chain = {"cuisine": RunnablePassthrough()} | prompt_template_name | llm

    # Chain 2 : Menu Items
    prompt_template_items = PromptTemplate(
        input_variables=["restaurant_name"],
        template="Suggest me some menu items for {restaurant_name}. Return it as a comma separated list.",
    )

    menu_items_chain = (
        {"restaurant_name": RunnablePassthrough()} | prompt_template_items | llm
    )

    full_chain = RunnableSequence(
        RunnablePassthrough().assign(restaurant_name=name_chain)
        | RunnablePassthrough().assign(menu_items=menu_items_chain)
    )

    response = full_chain.invoke({"cuisine": cuisine})

    return response
    # return response["restaurant_name"].content, response["menu_items"].content


# if __name__ == "__main__":
#     print(generate_restaurant_name_and_items("Italian"))
