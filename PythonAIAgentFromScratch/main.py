from specialized_rag import InvestedUserRAG, ReadyToInvestRAG, NoIdeaRAG
import os
import json
from dotenv import load_dotenv

def save_json_output(user_id: str, json_data: dict):
    """Save JSON output to a file."""
    os.makedirs("output", exist_ok=True)
    filename = f"output/user_{user_id}_investment_plan.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2)
    return filename

def main():
    # Load environment variables
    load_dotenv()

    # Initialize specialized RAG systems
    rag_systems = {
        'invested_user': InvestedUserRAG(),
        'ready_to_invest': ReadyToInvestRAG(),
        'no_idea': NoIdeaRAG()
    }
    
    print("Welcome to the Personalized Investment Advisor!")
    print("---------------------------------------------")
    print("Available User Types:")
    print("1. invested_user - Already invested in the market")
    print("2. ready_to_invest - Ready to start investing")
    print("3. no_idea - New to investing")
    
    while True:
        # Get user type
        print("\nSelect your user type (1/2/3) or type 'exit' to quit:")
        user_choice = input().strip().lower()
        
        if user_choice == 'exit':
            break
        
        user_type_map = {
            '1': 'invested_user',
            '2': 'ready_to_invest',
            '3': 'no_idea'
        }
        
        if user_choice not in user_type_map:
            print("Invalid choice. Please select 1, 2, or 3.")
            continue
        
        # Get user ID
        print("\nEnter your user ID:")
        user_id = input().strip()
        
        user_type = user_type_map[user_choice]
        rag = rag_systems[user_type]
        
        print(f"\nSelected User Type: {user_type}")
        print("Type 'profile' to view your profile")
        print("Type 'update' to update your profile")
        print("Type 'history' to view investment history")
        print("Type 'back' to select different user type")
        print("Type 'exit' to quit")
        
        while True:
            print("\nEnter your question or command:")
            query = input().strip().lower()
            
            if query == 'exit':
                return
            elif query == 'back':
                break
            elif query == 'profile':
                # Display user profile
                print(f"\nYour Profile ({user_type}):")
                print("This specialized RAG system is trained on data specific to your investment level.")
                continue
            elif query == 'update':
                print("\nProfile updates are handled through the specialized RAG system.")
                print("The system will automatically adjust recommendations based on your user type.")
                continue
            elif query == 'history':
                print("\nInvestment history is tracked through the specialized RAG system.")
                print("Recommendations are based on your user type and experience level.")
                continue
            
            # Get personalized recommendation using specialized RAG
            analysis, json_output = rag.get_personalized_recommendation(query, user_id)
            
            print("\nAnalysis:")
            print(analysis)
            
            if json_output:
                # Save JSON output to file
                output_file = save_json_output(user_id, json_output)
                print(f"\nDetailed investment plan saved to: {output_file}")
            
            print("\n" + "-"*50)

if __name__ == "__main__":
    main() 