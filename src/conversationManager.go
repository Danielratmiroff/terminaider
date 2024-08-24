package src

import (
	"fmt"
	"os"

	"github.com/Danielratmiroff/terminaider/api"
	"github.com/Danielratmiroff/terminaider/config"
	"github.com/Danielratmiroff/terminaider/prompts"
)

type ConversationManager struct {
	conversationHistory []string
	prompt              string
	g                   *api.Groq
}

func NewConversationManager(cfg *config.Config) *ConversationManager {
	if cfg.GroqAPIKey == "" {
		fmt.Println("GROQ_API_KEY is not set in the config")
		return nil
	}

	g := &api.Groq{ApiKey: cfg.GroqAPIKey}

	return &ConversationManager{
		conversationHistory: make([]string, 0),
		prompt:              prompts.DEFAULT_PROMPT,
		g:                   g,
	}
}

func (cm *ConversationManager) AddToConversationHistory(message string) {
	cm.conversationHistory = append(cm.conversationHistory, message)
}

func (cm *ConversationManager) GetConversationHistory() []string {
	return cm.conversationHistory
}

func (cm *ConversationManager) ComposePrompt(userInput string) string {
	return cm.prompt + "\n" + userInput
}

func (cm *ConversationManager) GetResponse(prompt string) (string, error) {
	return cm.g.ChatCompletion(prompt)
}
