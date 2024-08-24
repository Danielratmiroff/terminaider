package src

import (
	"bufio"
	"fmt"
	"os"
	"strings"

	"github.com/Danielratmiroff/terminaider/api"
	"github.com/Danielratmiroff/terminaider/config"
	"github.com/Danielratmiroff/terminaider/prompts"
	"github.com/charmbracelet/glamour"
)

func RunChat(cfg *config.Config) {
	cm := NewConversationManager(cfg)
	if cm == nil {
		return
	}

	fmt.Println("Welcome to the AI Chat Interface!")
	fmt.Println("Type 'exit' to quit.")

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

		prompt := cm.ComposePrompt(userInput)
		cm.AddToConversationHistory(userInput)
		response, err := cm.GetResponse(prompt)
		if err != nil {
			fmt.Printf("Error: %v\n", err)
			continue
		}

		// Render the response as Markdown
		out, err := glamour.Render(response, "dark")
		if err != nil {
			fmt.Printf("Error rendering Markdown: %v\n", err)
			continue
		}

		fmt.Println(out)
	}

	if err := scanner.Err(); err != nil {
		fmt.Printf("Error reading input: %v\n", err)
	}
}
