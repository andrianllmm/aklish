import React from "react";
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';


export default function Endgame({ show, isCorrect, solution, turn, numGuesses}) {
    return (
        <Modal
        show={show}
        size="lg"
        aria-labelledby="contained-modal-title-vcenter"
        centered
        >
            {isCorrect && 
            <>
                <Modal.Header>
                    <Modal.Title id="contained-modal-title-vcenter">
                        You guessed right!
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <h6>The word is "{solution}"</h6>
                    <p>
                    You got it right in {turn} guesses.
                    </p>
                </Modal.Body>
            </>
            }
            {!isCorrect && 
            <>
                <Modal.Header>
                    <Modal.Title id="contained-modal-title-vcenter">
                        You ran out of guesses!
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <h6>The word is "{solution}"</h6>
                    <p>
                    You got it right in {numGuesses} guesses.
                    </p>
                </Modal.Body>
            </>
            }
            <Modal.Footer>
                <Button href="/games/wordle">Next</Button>
            </Modal.Footer>
        </Modal>
    )
}
