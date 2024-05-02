import React from "react";
import { useParams } from "react-router-dom";
import Form from "react-bootstrap/Form";


export default function LanguageSelect() {
    const { lang } = useParams();

    function handleChange(event) {
        const selectedLang = event.target.value;
        window.location.href = `/games/wordle/${selectedLang}`;
    };

    return (
        <Form.Select value={lang} onChange={handleChange} style={{width: "25%", minWidth: "150px"}}>
            <option value="akl">Aklanon</option>
            <option value="eng">English</option>
        </Form.Select>
    );
}