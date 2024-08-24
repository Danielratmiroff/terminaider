package src

import (
	"bufio"
	"fmt"
	"os"
	"strings"

	"github.com/Danielratmiroff/terminaider/config"
	"github.com/charmbracelet/glamour"
)

func RunChat(cfg *config.Config, initialPrompt string) {
	cm := NewConversationManager(cfg)
	if cm == nil {
		return
	}

	fmt.Println("Welcome to the AI Chat Interface!")
	fmt.Println("Type 'exit' to quit.")

	if initialPrompt != "" {
		handleUserInput(cm, initialPrompt)
	}

	scanner := bufio.NewScanner(os.Stdin)
	for {
		fmt.Print("Enter your prompt: ")
		if !scanner.Scan() {
			break
		}
		userInput := scanner.Text()
		if strings.ToLower(userInput) == "exit" {
			break
		}

		handleUserInput(cm, userInput)
	}

	if err := scanner.Err(); err != nil {
		fmt.Printf("Error reading input: %v\n", err)
	}
}

func handleUserInput(cm *ConversationManager, userInput string) {
	prompt := cm.ComposePrompt(userInput)
	cm.AddUserMessage(userInput)
	fmt.Println(cm.GetConversationHistory())
	response, err := cm.GetResponse(prompt)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}

	// Render the response as Markdown
	out, err := glamour.Render(response, "dark")
	if err != nil {
		fmt.Printf("Error rendering Markdown: %v\n", err)
		return
	}

	fmt.Println(out)
}
