import React from "react";
import { useParams } from "react-router-dom";
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';


export default function Endgame({ show, isCorrect, solution, turn, numGuesses}) {
    const { lang } = useParams();

    return (
        <Modal
        show={show}
        size="sm"
        centered
        >
            {isCorrect && 
            <>
                <Modal.Header>
                    <Modal.Title>
                        You guessed right!
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <h6><a href={`/dictionary/${lang}/entry/${solution}`}>{solution}</a></h6>
                    <p>
                    You got it in {turn} guesses.
                    </p>
                </Modal.Body>
            </>
            }
            {!isCorrect && 
            <>
                <Modal.Header>
                    <Modal.Title>
                        You ran out of guesses!
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                <h6><a href={`/dictionary/${lang}/entry/${solution}`}>{solution}</a></h6>
                    <p>
                    You only have {numGuesses} guesses.
                    </p>
                </Modal.Body>
            </>
            }
            <Modal.Footer>
                <Button onClick={() => {window.location.reload()}}>Next</Button>
            </Modal.Footer>
        </Modal>
    )
}
