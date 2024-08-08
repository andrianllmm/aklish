import React from "react";
import Button from 'react-bootstrap/Button';


export default function Choices({ choices, onClick, selectedChoice, matchWord, answerSelected }) {
    return (
        <div className="d-flex flex-column m-2">
            {choices.map((choice, i) => (
                <Button key={i}
                    variant={
                        selectedChoice !== choice ?
                            (!answerSelected ?
                                "outline-primary" :
                                (choice !== matchWord ? "outline-primary" : "outline-success")) :
                            (selectedChoice === matchWord ? "success" : "danger")
                    }
                    className="mb-2 rounded-pill"
                    onClick={() => onClick(choice)}
                >
                    {choice}
                </Button>
            ))}
        </div>
    );
}