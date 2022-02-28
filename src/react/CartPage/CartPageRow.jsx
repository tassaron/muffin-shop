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
                className="CartPage-row row border-top d-flex align-items-center justify-content-center py-2"
                data-product-id={this.props.data.id}
            >
                <div className="CartPage-name col-12 text-center fs-3 product-title">
                    {this.props.data.name}
                </div>
                <div className="CartPage-image col-md-5 col-3">
                    <img
                        className="me-2 img-fluid rounded shadow-sm"
                        alt={this.props.data.name}
                        src={this.props.data.image}
                    />
                </div>
                <div className="CartPage-price d-flex justify-content-center col-2 pt-3">
                    {this.props.data.currency == "$"
                        ? "$" +
                          (
                              this.props.data.price * this.props.data.quantity
                          ).toFixed(2)
                        : this.props.data.price * this.props.data.quantity +
                          this.props.data.currency}
                </div>
                <div className="CartPage-quantity col-md-3 col-5">
                    <CartPageButtons
                        quantity={this.props.data.quantity}
                        stock={this.props.data.stock}
                        changed={this.props.data.changed}
                        setQuantityRelative={this.props.setQuantityRelative}
                    />
                </div>
                <div className="col-2">
                    <button
                        type="button"
                        onClick={() => this.props.removeMe(this.node)}
                        className="btn-default btn-round shadow-sm p-1"
                    >
                        🗑️
                    </button>
                </div>
            </div>
        );
    }
}

export default CartPageRow;
