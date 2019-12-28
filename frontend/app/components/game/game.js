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
                    {this.props.state}
                  </div>
                 )
        }
};
