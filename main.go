package main

import (
	"fmt"
	"os"
	"strings"

	"github.com/spf13/cobra"
	groq "github.com/Danielratmiroff/terminaider/go"
)

const DEFAULT_PROMPT = `
Act as an expert software developer. Always use best practices when coding. 
Be very concise, keep your responses straight to the point and be very clear in your responses.
Omit any unnecessary information and prerequisites.
You *MUST* use markdown and pay close attention to the formatting to make your response as clear as possible.
`

var rootCmd = &cobra.Command{
	Use:   "aider",
	Short: "AI Chat Interface",
	Run: func(cmd *cobra.Command, args []string) {
		apiKey := os.Getenv("GROQ_API_KEY")
		if apiKey == "" {
			fmt.Println("GROQ_API_KEY environment variable is not set")
			return
		}

		g := &groq.Groq{ApiKey: apiKey}

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

			prompt := DEFAULT_PROMPT + "\n" + userInput
			response, err := g.ChatCompletion(prompt)
			if err != nil {
				fmt.Printf("Error: %v\n", err)
				continue
			}

			fmt.Println("Response:", response)
		}

		if err := scanner.Err(); err != nil {
			fmt.Printf("Error reading input: %v\n", err)
		}
	},
}

func main() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}
	apiKey := os.Getenv("GROQ_API_KEY")
	if apiKey == "" {
		fmt.Println("GROQ_API_KEY environment variable is not set")
		return
	}

	g := &groq.Groq{ApiKey: apiKey}

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

		prompt := DEFAULT_PROMPT + "\n" + userInput
		response, err := g.ChatCompletion(prompt)
		if err != nil {
			fmt.Printf("Error: %v\n", err)
			continue
		}

		fmt.Println("Response:", response)
	}

	if err := scanner.Err(); err != nil {
		fmt.Printf("Error reading input: %v\n", err)
	}
}
