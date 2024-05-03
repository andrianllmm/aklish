import React from "react";
import { useParams } from "react-router-dom";
import Header from "../../Header";
import Message from "../Message";
import Choices from "./Choices";
import Button from "react-bootstrap/Button";


export default function Match() {
    const wordLen = [3, 10];
    const [lang, setLang] = React.useState(useParams().lang);
    const [word, setWord] = React.useState("");
    const [matchWord, setMatchWord] = React.useState("");
    const [choices, setChoices] = React.useState([]);
    const [selectedChoice, setSelectedChoice] = React.useState(null);
    const [isCorrect, setIsCorrect] = React.useState(null);
    const [answerSelected, setAnswerSelected] = React.useState(false);
    const [message, setMessage] = React.useState(null);

    React.useEffect(() => {
        fetch(
            `/dictionary/api/${lang}/entry/?` + 
            `has=similar&` +
            `word_len=${wordLen[0]}-${wordLen[1]}&` +
            `classification!=vul&`
        )
            .then(response => response.json())
            .then(data => {
                setWord(data.word.toLowerCase());

                const attributes = data.attributes;
                let similar_list = [];
                for (const attribute of attributes) {
                    similar_list.push(...attribute.similar);
                }
                similar_list = similar_list.filter(Boolean);
                const similar_word = similar_list[Math.floor(Math.random() * similar_list.length)];
                setMatchWord(similar_word.toLowerCase());
            });
    }, []);

    React.useEffect(() => {
        fetch(
            `/dictionary/api/${lang}/entries/?` + 
            `num=3&`
        )
            .then(response => response.json())
            .then(data => {
                for (let entry of data) {
                    setChoices((prev) => {
                        return [...prev, entry.word.toLowerCase()].sort(() => Math.random() - 0.5);
                    });
                }
            });
    }, []);

    React.useEffect(() => {
        { matchWord &&
            setChoices((prev) => {
                return [...prev, matchWord.toLocaleLowerCase()].sort(() => Math.random() - 0.5);
            });
        }
    }, [matchWord]);

    // React.useEffect(() => {
    //     if (isCorrect !== null) {
    //         if (isCorrect) {
    //             setMessage(["Correct", "info"]);
    //         } else {
    //             setMessage(["Incorrect", "info"]);
    //         }
    //     }
    // }, [isCorrect]);

    const handleChoiceClick = (choice) => {
        if (!answerSelected) {
            setSelectedChoice(choice);
            setIsCorrect(choice === matchWord);
            setAnswerSelected(true);
        }
    };

    return (
        <>
            {word && ( 
                <>
                    <Header title="Match" />
                    <div className="d-flex flex-column align-items-center text-center">
                        <div>
                            <h1 className="m-2 fs-3">Which is similar to <strong>{word}</strong>?</h1>
                        </div>
                        {message &&
                            <Message message={message[0]} variant={message[1]}/>
                        }
                        <Choices choices={choices} onClick={handleChoiceClick} selectedChoice={selectedChoice} matchWord={matchWord} answerSelected={answerSelected} />
                        <Button onClick={() => {window.location.reload()}}>Next</Button>
                    </div>
                </>
            )}
        </>
    )
}