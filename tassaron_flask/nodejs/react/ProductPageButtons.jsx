/* This component receives the product stock data as a prop
* And handles the quantity of the add-to-cart helper button
*/
import React, { Component } from "react";


class ProductPageButtons extends Component {
    constructor(props) {
        super(props);
        this.state = {
            cartQuantity: this.props.initialQuantity,
            quantity: 0
        }
    }

    render() {
        function downBtnEnabled(state) {
            return state.quantity > 0;
        };

        function upBtnEnabled(state, props) {
            return state.quantity + state.cartQuantity < props.stock;
        };


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
                <div style={{ position: "absolute", bottom: "-1.375rem", fontSize: "0.8rem", width: "100%" }} className="text-center"><strong>{this.state.cartQuantity}</strong> in your cart</div>
            </div>
        )
    }
}

export default ProductPageButtons