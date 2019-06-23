import React from 'react';
import ReactDOM from 'react-dom';
import axios from "axios";
import './bulma.css';

function Input(props) {
    return (
        <div className="field">
            <label className="label" htmlFor={props.id}>{props.label}</label>
            <div className="control">
                <input
                    id={props.id}
                    className="input"
                    type={props.type}
                    value={props.value}
                    placeholder={props.placeholder}
                    onChange={props.onChange}
                />
            </div>
        </div>
    )
}

function Button(props) {
    return (
        <div className="control">
            <button className={"button " + props.className} onClick={props.onClick}>{props.label}</button>
        </div>
    )
}

class Login extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            username: '',
            password: '',
            note: null,
        };
    }

    note(props) {
        return (<div className={"notification " + props.className}>
            <span>{props.status_code}</span><p>{props.content}</p>
        </div>)
    }

    handleClick(e) {
        e.preventDefault();
        axios.post('http://localhost:4000/login', { username: this.state.username, password: this.state.password })
            .then(
                (res) => {
                    this.setState({
                        note: this.note({className: 'is-info', status_code: res.status, content: res.data})
                    });
                },
            )
            .catch(
                (err) => {
                    this.setState({
                        note: this.note({className: 'is-warning', status_code: err.response.status, content: err.response.data})
                    });
                }
            );
    }

    render() {
        return (
            <div className="column">
                <form className="form">
                    <Input
                        id="username"
                        type="text"
                        label="ユーザー名"
                        value={this.state.username}
                        onChange={(e) => this.setState({username: e.target.value})}
                    />
                    <Input
                        id="password"
                        type="password"
                        label="パスワード"
                        value={this.state.password}
                        onChange={(e) => this.setState({password: e.target.value})}
                    />
                    <Button className="is-link" label="ログイン" onClick={(e) => this.handleClick(e)} />
                </form>
                {this.state.note}
            </div>
        )
    }
}

function App(props) {
    return (
        <section className="section">
            <div className="container">
                <div className="columns">
                    <Login />
                </div>
            </div>
        </section>
    )
}

// ========== main ==========
ReactDOM.render(
    <App />,
    document.getElementById('root')
);
