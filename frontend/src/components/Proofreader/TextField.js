import React from "react";

export default function TextField({ textInput, textMarks, handleInputChange }) {
    const syncScrollPositions = () => {
        const textArea = document.querySelector("#proofreader-text-area");
        const textMarks = document.querySelector("#proofreader-text-marks");

        if (textArea && textMarks) {
            textMarks.scrollTop = textArea.scrollTop;
            console.log(textArea.scrollTop)
            console.log(textMarks.scrollTop)
        }
    };

    const handleTextScroll = () => {
        syncScrollPositions();
    };

    return (
        <div className="form-group">
            <div id="proofreader-text-area">
                <textarea
                    name="content"
                    value={textInput}
                    id="proofreader-text-input"
                    cols="30"
                    rows="10"
                    placeholder="Start writing here."
                    className="form-control px-4 py-3 m-0"
                    maxLength="300"
                    required
                    onChange={handleInputChange}
                    onScroll={handleTextScroll}
                ></textarea>
                <div
                    id="proofreader-text-marks"
                    className="form-control px-4 py-3 m-0"
                    dangerouslySetInnerHTML={{ __html: textMarks }}
                ></div>
            </div>
        </div>
    );
}
