import { Component } from "react";
import { animateVanish } from "./util.js";


const ANIMSPEED = 3000;


class CartQuantityUpdater extends Component {
    constructor(props) {
        super(props);
        this.vanishing = false;
    }

    componentDidMount() {
        this.watchedNode = document.querySelector(
            `.ProductPage-alert-area[data-product-id='${this.props.productId}']`
        );
        this.timer = setInterval(() => this.tick(), ANIMSPEED);
    }
    componentWillUnmount() {
        clearInterval(this.timer);
    }

    tick() {
        if (this.watchedNode.childElementCount == 0 || this.vanishing) {
            return;
        }
        this.vanishing = true;
        const child = this.watchedNode.children[0];
        const message = child.innerText;
        const newValue = Number(message.split(" ")[1]);
        const doAnimation = () => {
            requestAnimationFrame(() =>
                animateVanish(
                    child,
                    () => {
                        this.vanishing = false;
                        this.watchedNode.removeChild(child);
                    }
                )
            );
            this.props.setQuantityFunc(this.props.initialQuantity + newValue);
            this.props.cartBtn.classList.remove("btn-disabled");
        }
        // Trigger animation ANIMSPEED milliseconds after node creation 
        setTimeout(doAnimation, Math.min(Date.now() - (Number(child.dataset.timestamp) + ANIMSPEED), 0))
    }

    render() {
        return (
            <div
                style={{
                    visibility:
                        this.props.initialQuantity > 0 ? "visible" : "hidden",
                }}
                className="product-buttons-cart-indicator-text text-center"
            >
                <strong>{this.props.initialQuantity}</strong> in your cart
            </div>
        );
    }
}

export default CartQuantityUpdater;
