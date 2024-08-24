package groq

import (
	"net/http"
	"io/ioutil"
)

type Groq struct {
	ApiKey string
}

func (g *Groq) ChatCompletion(prompt string) (string, error) {
	// TO DO: implement HTTP request to Groq API
	return "", nil
}
