import React from 'react';
import ReactDOM from 'react-dom';

class App extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            state: null,
            gameId: null,
        };

        this.newGame = this.newGame.bind(this);
        this.updateState = this.updateState.bind(this);
    }

    componentDidMount() {
        this.updateState();
    }

    updateState() {
        if (this.state.gameId != null) {
            const encodedGameId = encodeURIComponent(this.state.gameId);
            fetch(`http://localhost:4800/api/state?gameId=${encodedGameId}`)
                .then(res => res.json())
                .then((data) => {
                  this.setState({ state: data });
                })
                .catch(console.log)
        }
    }

    newGame() {
        fetch('http://localhost:4800/api/game')
            .then(res => res.json())
            .then((data) => {
              this.setState({ gameId: data });
              this.updateState();
            })
            .catch(console.log)
    }

    render() {
          return (
                  <div>
                    <button onClick={this.newGame}>New game</button>
                    <button onClick={this.updateState}>Update</button>
                    <br/>
                    <game state=this.state.state></game>
                  </div>
                 )
        }
};

ReactDOM.render(<App />, document.getElementById('app'));