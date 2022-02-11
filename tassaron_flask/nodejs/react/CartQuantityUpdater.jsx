import { Component } from "react";
import { animateVanish } from './util.js';


class CartQuantityUpdater extends Component {
    constructor(props) {
        super(props);
        this.vanishing = false;
    }

    componentDidMount() {
        this.watchedNode = document.querySelector(`.ProductPage-alert-area[data-product-id='${this.props.productId}']`);
        this.timer = setInterval(
            () => this.tick(),
            3000
        );
    }
    componentWillUnmount() {
        clearInterval(this.timer);
    }

    tick() {
        if (this.watchedNode.childElementCount == 0 || this.vanishing) {
            return
        }
        this.vanishing = true;
        const child = this.watchedNode.children[0];
        const message = child.innerText;
        const newValue = Number(message.split(" ")[1]);
        requestAnimationFrame(
            () => animateVanish(child, this.watchedNode, () => this.vanishing = false)
        );
        this.props.setQuantityFunc(this.props.initialQuantity + newValue);
        this.props.cartBtn.classList.remove("btn-disabled");
    }

    render() {
        return (
            <div
                style={{ visibility: this.props.initialQuantity > 0 ? "visible" : "hidden" }}
                className="product-buttons-cart-indicator-text text-center">
                <strong>
                    {this.props.initialQuantity}
                </strong> in your cart
            </div>
        )
    }
}

export default CartQuantityUpdater