package main

import (
	"fmt"
	"os"
	"strings"
)

const DEFAULT_PROMPT = `
Act as an expert software developer. Always use best practices when coding. 
Be very concise, keep your responses straight to the point and be very clear in your responses.
Ommit any unnecessary information and prerequisites.
You *MUST* use markdown and pay close attention to the formatting to make your response as clear as possible.
`

func getGroqResponse(prompt string) string {
	// TO DO: implement Groq API call
	return ""
}

func main() {
	fmt.Println("Welcome to the AI Chat Interface!")
	for {
		var userInput string
		fmt.Print("Enter your prompt: ")
		fmt.Scanln(&userInput)
		if strings.ToLower(userInput) == "exit" {
			break
		}
		response := getGroqResponse(userInput)
		fmt.Println(response)
	}
}
