import React from "react";


export default function({ textInput, textMarks, handleInputChange }) {
    return (
        <div className="form-group">
            <div id="proofreader-field">
                <textarea
                    value={textInput}
                    id="proofreader-text-input"
                    cols="30"
                    rows="10"
                    placeholder="Start writing here."
                    autoFocus
                    className="form-control px-4 py-3 m-0"
                    onChange={handleInputChange}
                ></textarea>
                <div
                    id="proofreader-text-marks"
                    className="form-control px-4 py-3 m-0"
                    dangerouslySetInnerHTML={{ __html: textMarks }}
                ></div>
            </div>
        </div>
    )
}