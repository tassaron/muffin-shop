/* This component receives the product stock data as a prop
* And handles the quantity of the add-to-cart helper button
*/
import React, { Component } from "react";
import CartQuantityUpdater from "./CartQuantityUpdater";


class ProductPageButtons extends Component {
    constructor(props) {
        super(props);
        this.state = {
            quantity: 0,
            cartBtn: null
        }
    }

    componentDidMount() {
        this.setState({
            cartBtn: document.querySelector(`.ProductPage-cart-btn-${this.props.productId}[data-product-id='${this.props.productId}']`)
        });
    }

    render() {
        if (this.state.cartBtn === null) return null
        function downBtnEnabled(state) {
            return state.quantity > 0;
        };

        function upBtnEnabled(state, props) {
            return state.quantity + props.initialQuantity < props.stock;
        };

        if (this.state.quantity < 1) {
            this.state.cartBtn.classList.add("btn-disabled");
        } else {
            this.state.cartBtn.classList.remove("btn-disabled");
        }

        return (
            <div class="btn-group" role="group" aria-label="product quantity">
                <div className={downBtnEnabled(this.state) ? "btn-enabled" : "btn-disabled"}
                    dangerouslySetInnerHTML={{__html: this.props.downBtn}}
                    onClick={
                        () => {
                            this.setState((state, props) => {
                                if (downBtnEnabled(state)) {
                                    return {quantity: state.quantity - 1}
                                }
                            });
                        }
                    }
                    />
                <div className={
                        downBtnEnabled(this.state) || upBtnEnabled(this.state, this.props) ? (
                            "ProductPage-quantity p-3 btn-enabled" 
                        ) : (
                            "ProductPage-quantity p-3 btn-disabled"
                        )
                    }
                    data-product-id={this.props.productId}
                    >
                    {this.state.quantity}
                </div>
                <div className={upBtnEnabled(this.state, this.props) ? "btn-enabled" : "btn-disabled"}
                    dangerouslySetInnerHTML={{__html: this.props.upBtn}}
                    onClick={
                        () => {
                            this.setState((state, props) => {
                                if (upBtnEnabled(state, props)) {
                                    return {quantity: state.quantity + 1}
                                }
                            });
                        }
                    }
                    />
                <CartQuantityUpdater cartBtn={this.state.cartBtn} productId={this.props.productId} initialQuantity={this.props.initialQuantity} />
            </div>
        )
    }
}

export default ProductPageButtons