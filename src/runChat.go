package src

import (
	"bufio"
	"fmt"
	"os"
	"strings"

	"github.com/Danielratmiroff/terminaider/api"
	"github.com/Danielratmiroff/terminaider/prompts"
	"github.com/charmbracelet/glamour"
	"github.com/spf13/cobra"
)

func RunChat(cmd *cobra.Command, args []string) {
	apiKey := os.Getenv("GROQ_API_KEY")
	if apiKey == "" {
		fmt.Println("GROQ_API_KEY environment variable is not set")
		return
	}

	g := &api.Groq{ApiKey: apiKey}

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

		prompt := prompts.DEFAULT_PROMPT + "\n" + userInput
		response, err := g.ChatCompletion(prompt)
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
