package main

import (
	"fmt"
	"log"

	"github.com/mattn/go-tty"
)

func HandleKeystrokes(keys chan *string) {
	// Open a new TTY
	tty, err := tty.Open()
	if err != nil {
		log.Fatalf("Failed to open TTY: %v", err)
	}
	defer tty.Close()

	fmt.Println("Press arrow keys or other keys (Ctrl+C to exit)")

	for {
		// Read a single key press
		r, err := tty.ReadRune()
		if err != nil {
			log.Fatalf("Error reading from TTY: %v", err)
		}
		output := ""
		switch r {
		case 27: // Escape character for special keys
			// Check for multi-character sequences (e.g., arrow keys)
			next1, _ := tty.ReadRune()
			if next1 == '[' {
				next2, _ := tty.ReadRune()
				switch next2 {
				case 'A':
					output = "^"
					keys <- &output
					continue
				case 'B':
					output = "v"
					keys <- &output
					continue
				case 'C':
					output = ">"
					keys <- &output
					continue
				case 'D':
					output = "<"
					keys <- &output
					continue
				default:
					fmt.Printf("Unknown sequence: [%c%c]\n", next1, next2)
				}
			}
		case 'q': // Example key for quitting
			fmt.Println("Exiting on 'q'")
			close(keys)
			return
		default:
			// Handle other keys
			output = string(r)
			keys <- &output
		}
	}
}

