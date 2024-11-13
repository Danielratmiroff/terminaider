package src

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"regexp"
	"strings"

	"github.com/Danielratmiroff/terminaider/config"
	"github.com/Danielratmiroff/terminaider/prompts"
	"github.com/atotto/clipboard"
	"github.com/charmbracelet/glamour"
)

func RunChat(cfg *config.Config, initialPrompt string) {
	cm := NewConversationManager(cfg)
	if cm == nil {
		return
	}

	fmt.Println("** Welcome to the AI Chat Interface!")

	if initialPrompt != "" {
		if cfg.PromptType == prompts.DEFAULT {
			handleUserInput(cm, initialPrompt)
		} else {
			handleUserInputAsExecutable(cm, initialPrompt)
		}
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

		if cfg.PromptType == prompts.DEFAULT {
			handleUserInput(cm, userInput)
		} else {
			handleUserInputAsExecutable(cm, userInput)
		}
	}

	if err := scanner.Err(); err != nil {
		fmt.Printf("Error reading input: %v\n", err)
	}
}

func handleUserInput(cm *ConversationManager, userInput string) {
	prompt := cm.ComposePrompt(userInput)
	cm.AddUserMessage(userInput)
	response, err := cm.GetResponse(prompt)
	if err != nil {
		log.Fatal(err)
	}

	// Render the full response as Markdown
	out, err := glamour.Render(response, "dark")
	if err != nil {
		log.Fatalf("Error rendering Markdown: %v\n", err)
	}

	fmt.Println(out)
}

func handleUserInputAsExecutable(cm *ConversationManager, userInput string) {
	prompt := cm.ComposePrompt(userInput)
	cm.AddUserMessage(userInput)
	response, err := cm.GetResponse(prompt)
	if err != nil {
		log.Fatal(err)
	}

	// Render the full response as Markdown
	out, err := glamour.Render(response, "dark")
	if err != nil {
		log.Fatalf("Error rendering Markdown: %v\n", err)
	}

	fmt.Println(out)

	// Extract content inside <code> tags
	re := regexp.MustCompile(`(?s)<code>(.*?)</code>`)
	matches := re.FindStringSubmatch(response)

	if len(matches) > 1 {
		codeContent := strings.TrimSpace(matches[1])
		// Copy the code content to clipboard
		if err := clipboard.WriteAll(codeContent); err != nil {
			fmt.Printf("Error copying to clipboard: %v\n", err)
		} else {
			in := fmt.Sprintf("_Copied_: ```%s ```", codeContent)
			out, err := glamour.Render(in, "dark")

			if err != nil {
				log.Fatal(err)
			}

			fmt.Print(out)
		}
	} else {
		fmt.Println("No code block found in the response.")
	}
}
