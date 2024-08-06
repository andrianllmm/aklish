import React from "react";
import { Link, useLocation, useParams, useNavigate } from "react-router-dom";
import Form from "react-bootstrap/Form";
import Dropdown from 'react-bootstrap/Dropdown';
import DropdownButton from 'react-bootstrap/DropdownButton';

export default function LanguageSelect() {
    const { lang } = useParams();

    const location = useLocation();
    const parentPath = location.pathname.split("/").filter(Boolean).slice(0, -1).join("/");

    const navigate = useNavigate();

    function handleChange(event) {
        const selectedLang = event.target.value;
        navigate(`../${parentPath}/${selectedLang}`);
        navigate(0);
    };

    return (
        <Form.Select value={lang} onChange={handleChange} style={{width: "25%", minWidth: "150px"}}>
            <option value="akl">Aklanon</option>
            <option value="eng">English</option>
        </Form.Select>
    );
}