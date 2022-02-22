/* This component receives the product stock data as a prop
 * It tracks the quantity of product in the cart, from 0 to stock
 * Disables/enables the -/+ buttons and updates the displayed price
 */
import React, { Component } from "react";

class CartPageButtons extends Component {
    render() {
        return (
            <div
                className="btn-group"
                role="group"
                aria-label="quantity in cart"
            >
                <button
                    type="button"
                    onClick={() => {
                        if (this.props.quantity > 0)
                            this.props.setQuantityRelative(-1);
                    }}
                    className={
                        this.props.quantity > 0
                            ? "CartPage-quantity-down btn btn-secondary shadow-sm p-3"
                            : "CartPage-quantity-down btn btn-secondary shadow-sm p-3 btn-disabled"
                    }
                >
                    -
                </button>
                <div className="CartPage-quantity p-3 fs-5">
                    {this.props.changed ? (
                        <span className="text-danger">
                            {this.props.quantity}
                        </span>
                    ) : (
                        <span className="text-dark">{this.props.quantity}</span>
                    )}
                </div>
                <button
                    type="button"
                    onClick={() => {
                        if (this.props.quantity < this.props.stock)
                            this.props.setQuantityRelative(1);
                    }}
                    className={
                        this.props.quantity < this.props.stock
                            ? "CartPage-quantity-up btn btn-secondary p-3"
                            : "CartPage-quantity-up btn btn-secondary p-3 btn-disabled"
                    }
                >
                    +
                </button>
            </div>
        );
    }
}

export default CartPageButtons;
