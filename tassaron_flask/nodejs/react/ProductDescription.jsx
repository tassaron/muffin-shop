import React, { Component } from "react";


class ProductDescription extends Component {
    constructor(props) {
        super();
    }

    render() {
        return (
            <div className="col">
                {this.props.content}
            </div>
        )
    }

}

export default ProductDescription