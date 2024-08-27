package src

import (
	"fmt"

	"github.com/Danielratmiroff/terminaider/api"
	"github.com/Danielratmiroff/terminaider/config"
	"github.com/Danielratmiroff/terminaider/prompts"
)

type ConversationManager struct {
	userHistory   []string
	aiHistory     []string
	prompt        string
	g             *api.Groq
	windowHistory int
}

func NewConversationManager(cfg *config.Config) *ConversationManager {
	if cfg.GroqAPIKey == "" {
		fmt.Println("GROQ_API_KEY is not set in the config")
		return nil
	}

	g := &api.Groq{ApiKey: cfg.GroqAPIKey}

	var prompt string
	if cfg.PromptType == prompts.EXECUTE {
		prompt = prompts.DEFAULT_PROMPT + prompts.EXECUTE_PROMPT
	} else {
		prompt = prompts.DEFAULT_PROMPT
	}

	return &ConversationManager{
		userHistory:   make([]string, 0),
		aiHistory:     make([]string, 0),
		prompt:        prompt,
		g:             g,
		windowHistory: 3,
	}
}

func (cm *ConversationManager) AddUserMessage(message string) {
	cm.userHistory = append(cm.userHistory, message)
}

func (cm *ConversationManager) AddAIMessage(message string) {
	cm.aiHistory = append(cm.aiHistory, message)
}

func (cm *ConversationManager) GetConversationHistory() ([]string, []string) {
	return cm.userHistory, cm.aiHistory
}

func (cm *ConversationManager) ComposePrompt(userInput string) string {
	// Get the last 3 messages from both user and AI history
	userMessages := cm.getLastNMessages(cm.userHistory, cm.windowHistory)
	aiMessages := cm.getLastNMessages(cm.aiHistory, cm.windowHistory)

	// Combine the messages into the prompt
	combinedMessages := ""
	for i := 0; i < len(userMessages); i++ {
		combinedMessages += "User: " + userMessages[i] + "\n"
		if i < len(aiMessages) {
			combinedMessages += "AI: " + aiMessages[i] + "\n"
		}
	}
	combinedMessages += "User: " + userInput
	return cm.prompt + "\n" + combinedMessages
}

func (cm *ConversationManager) getLastNMessages(messages []string, n int) []string {
	if len(messages) <= n {
		return messages
	}
	return messages[len(messages)-n:]
}

func (cm *ConversationManager) GetResponse(prompt string) (string, error) {
	response, err := cm.g.ChatCompletion(prompt)
	if err != nil {
		return "", err
	}
	cm.AddAIMessage(response)
	return response, nil
}
