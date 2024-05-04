import React from "react";


export default function({ textInput, textMarks, handleInputChange }) {
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
                    required
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