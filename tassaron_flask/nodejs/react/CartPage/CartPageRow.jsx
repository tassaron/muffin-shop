import React, { Component } from "react";
import CartPageButtons from "./CartPageButtons";

class CartPageRow extends Component {
    constructor(props) {
        super(props);
        this.node = React.createRef();
    }

    render() {
        return (
            <div
                ref={this.node}
                className="CartPage-row row border-top py-2"
                data-product-id={this.props.data.id}
            >
                <div className="CartPage-name col-12 text-center text-uppercase product-title">
                    {this.props.data.name}
                </div>
                <div className="CartPage-image col-md-5 col-3">
                    <img
                        width="fit-content"
                        className="mr-2 img-fluid rounded shadow-sm"
                        alt={this.props.data.name}
                        src={this.props.data.image}
                    />
                </div>
                <div className="CartPage-price col-2">
                    ${this.props.data.price.toFixed(2)}
                </div>
                <div className="CartPage-quantity col-md-3 col-5">
                    <CartPageButtons
                        quantity={this.props.data.quantity}
                        stock={this.props.data.stock}
                        changeQuantity={this.props.changeQuantity}
                    />
                </div>
                <div className="col-2">
                    <a
                        onClick={() => this.props.removeMe(this.node)}
                        className="btn"
                    >
                        🗑️
                    </a>
                </div>
            </div>
        );
    }
}

export default CartPageRow;
