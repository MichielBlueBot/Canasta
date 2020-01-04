import React from 'react';
import ReactDOM from 'react-dom';

class Game extends React.Component {

    constructor(props) {
        super(props);
    }

    componentDidMount() {
    }

    render() {
          return (
                     <div>
                         <GameStateText state={JSON.parse(this.props.state)}/>
                         <canvas id="myCanvas" width="1080px" height="720px" style={{border:'1px solid #000000'}}></canvas>);
                      </div>
                 )
        }
};

function GameStateText(props) {
    if (props.state != null){
        return (<div>
                  <ul>
                      <li>PHASE: {props.state.phase}</li>
                      <li>CURRENT PLAYER: {props.state.players[props.state.currentPlayerIndex].playerId}</li>
                      <li>DECK: {props.state.deck.numCards} cards</li>
                      <li>STACK: {props.state.stack.numCards} cards | top = ({props.state.stack.topCard.rank} {props.state.stack.topCard.suit})</li>
                      <li>LEFT PILE: {props.state.leftPile.numCards} cards (active={props.state.leftPile.active.toString()})</li>
                      <li>RIGHT PILE: {props.state.rightPile.numCards} cards (active={props.state.rightPile.active.toString()})</li>
                  </ul>
                </div>);
    }
    return null;
}
// Make this component available to other components
export default Game;
