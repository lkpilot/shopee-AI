from services.answer_question import answer_question
import asyncio
import warnings
warnings.filterwarnings("ignore")

async def main():
    while True:
        question = input("Enter your question: ")
        if question == "q":
            break
        result = await answer_question(question)
        print(result)
        print("\n")


if __name__ == "__main__":
    asyncio.run(main())
