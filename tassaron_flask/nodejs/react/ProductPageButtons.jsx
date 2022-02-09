/* This component gets the product stock data from the HTML
*  It handles the plus/minus buttons, add to cart button, and cart number in navbar
*  We do API requests to the "shop.add_product_to_cart" route
*/
import React, { Component } from "react";
import getNodeOrError from "./util";


class ProductPageButtons extends Component {
    constructor(props) {
        super(props);
        this.state = {
            quantity: this.props.initialQuantity
        }
    }

    render() {
        return (
            <div class="btn-group" role="group" aria-label="product quantity">
                <div dangerouslySetInnerHTML={{__html: this.props.downBtn}}
                    onClick={
                        () => {
                            this.setState((state, props) => {
                                if (state.quantity > 0) {
                                    return {quantity: state.quantity - 1}
                                }
                            });
                        }
                    }
                    />
                <div id="ProductPage-quantity" class="p-3">{this.state.quantity}</div>
                <div dangerouslySetInnerHTML={{__html: this.props.upBtn}}
                    onClick={
                        () => {
                            this.setState((state, props) => {
                                if (state.quantity < props.stock) {
                                    return {quantity: state.quantity + 1}
                                }
                            });
                        }
                    }
                    />
            </div>
        )
    }
}

export default ProductPageButtons