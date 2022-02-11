/* This component receives the product stock data as a prop
* And handles the quantity of the add-to-cart helper button
*/
import React, { Component } from "react";
import CartQuantityUpdater from "./CartQuantityUpdater";


class ProductPageButtons extends Component {
    constructor(props) {
        super(props);
        this.state = {
            buttonQuantity: 0,
            cartQuantity: props.initialQuantity,
            cartBtn: null
        }
    }

    setCartQuantity = (value) => {
        this.setState((state, props) => ({
            cartQuantity: value,
            buttonQuantity: Math.min(state.buttonQuantity, props.stock - value)
        }));
    }

    componentDidMount() {
        this.setState({
            cartBtn: document.querySelector(`.ProductPage-cart-btn-${this.props.productId}[data-product-id='${this.props.productId}']`)
        });
    }

    render() {
        if (this.state.cartBtn === null) return null
        function downBtnEnabled(state) {
            return state.buttonQuantity > 0;
        };

        function upBtnEnabled(state, props) {
            return state.buttonQuantity + state.cartQuantity < props.stock;
        };

        if (this.state.buttonQuantity < 1) {
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
                                    return {buttonQuantity: state.buttonQuantity - 1}
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
                    {this.state.buttonQuantity}
                </div>
                <div className={upBtnEnabled(this.state, this.props) ? "btn-enabled" : "btn-disabled"}
                    dangerouslySetInnerHTML={{__html: this.props.upBtn}}
                    onClick={
                        () => {
                            this.setState((state, props) => {
                                if (upBtnEnabled(state, props)) {
                                    return {buttonQuantity: state.buttonQuantity + 1}
                                }
                            });
                        }
                    }
                    />
                <CartQuantityUpdater
                    cartBtn={this.state.cartBtn}
                    productId={this.props.productId}
                    initialQuantity={this.state.cartQuantity}
                    setQuantityFunc={this.setCartQuantity} />
            </div>
        )
    }
}

export default ProductPageButtons