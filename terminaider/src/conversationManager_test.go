package src

import (
	"testing"

	"github.com/Danielratmiroff/terminaider/config"
	"github.com/Danielratmiroff/terminaider/prompts"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

type MockGroq struct {
	mock.Mock
}

func (m *MockGroq) ChatCompletion(prompt string) (string, error) {
	args := m.Called(prompt)
	return args.String(0), args.Error(1)
}

func TestNewConversationManager(t *testing.T) {
	cfg := &config.Config{GroqAPIKey: "test_key"}
	cm := NewConversationManager(cfg)

	assert.NotNil(t, cm)
	assert.Equal(t, 0, len(cm.userHistory))
	assert.Equal(t, 0, len(cm.aiHistory))
	assert.Equal(t, prompts.DEFAULT_PROMPT, cm.prompt)
	assert.Equal(t, "test_key", cm.g.ApiKey)
}

func TestAddUserMessage(t *testing.T) {
	cfg := &config.Config{GroqAPIKey: "test_key"}
	cm := NewConversationManager(cfg)

	cm.AddUserMessage("Hello")
	assert.Equal(t, 1, len(cm.userHistory))
	assert.Equal(t, "Hello", cm.userHistory[0])
}

func TestAddAIMessage(t *testing.T) {
	cfg := &config.Config{GroqAPIKey: "test_key"}
	cm := NewConversationManager(cfg)

	cm.AddAIMessage("Hi there")
	assert.Equal(t, 1, len(cm.aiHistory))
	assert.Equal(t, "Hi there", cm.aiHistory[0])
}

func TestGetConversationHistory(t *testing.T) {
	cfg := &config.Config{GroqAPIKey: "test_key"}
	cm := NewConversationManager(cfg)

	cm.AddUserMessage("Hello")
	cm.AddAIMessage("Hi there")

	userHistory, aiHistory := cm.GetConversationHistory()
	assert.Equal(t, 1, len(userHistory))
	assert.Equal(t, "Hello", userHistory[0])
	assert.Equal(t, 1, len(aiHistory))
	assert.Equal(t, "Hi there", aiHistory[0])
}

func TestComposePrompt(t *testing.T) {
	cfg := &config.Config{GroqAPIKey: "test_key"}
	cm := NewConversationManager(cfg)

	cm.AddUserMessage("Hello")
	cm.AddAIMessage("Hi there")
	prompt := cm.ComposePrompt("How are you?")

	expectedPrompt := cm.prompt + "\nUser: Hello\nAI: Hi there\nUser: How are you?"
	assert.Equal(t, expectedPrompt, prompt)
}

func TestGetLastNMessages(t *testing.T) {
	cfg := &config.Config{GroqAPIKey: "test_key"}
	cm := NewConversationManager(cfg)

	messages := []string{"msg1", "msg2", "msg3", "msg4"}
	result := cm.getLastNMessages(messages, 2)

	assert.Equal(t, []string{"msg3", "msg4"}, result)
}

// TODO: finalise these tests
// func TestGetResponse(t *testing.T) {
// 	cfg := &config.Config{GroqAPIKey: "test_key"}
// 	cm := NewConversationManager(cfg)

// 	// Create a mock Groq struct
// 	mockGroq := new(MockGroq)

// 	// Set up expectations
// 	mockGroq.On("ChatCompletion", "Test prompt").Return("Mocked response", nil)

// 	// Assign the mock to cm.g
// 	cm.g = mockGroq

// 	response, err := cm.GetResponse("Test prompt")
// 	assert.NoError(t, err)
// 	assert.Equal(t, "Mocked response", response)
// 	assert.Equal(t, 1, len(cm.aiHistory))
// 	assert.Equal(t, "Mocked response", cm.aiHistory[0])

// 	mockGroq.AssertExpectations(t)
// }

// func TestGetResponseError(t *testing.T) {
// 	cfg := &config.Config{GroqAPIKey: "test_key"}
// 	cm := NewConversationManager(cfg)

// 	// Create a mock Groq struct
// 	mockGroq := new(MockGroq)

// 	// Set up expectations for an error case
// 	mockGroq.On("ChatCompletion", "Test prompt").Return("", fmt.Errorf("mock error"))

// 	// Assign the mock to cm.g
// 	cm.g = mockGroq

// 	response, err := cm.GetResponse("Test prompt")
// 	assert.Error(t, err)
// 	assert.Equal(t, "", response)
// 	assert.Equal(t, 0, len(cm.aiHistory))

// 	mockGroq.AssertExpectations(t)
// }
