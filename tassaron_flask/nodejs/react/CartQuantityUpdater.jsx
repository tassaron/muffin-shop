import { Component } from "react";

let then = Date.now();

class CartQuantityUpdater extends Component {
    constructor(props) {
        super(props);
        this.state = {
            quantity: this.props.initialQuantity
        }
        this.vanishing = false;
    }

    componentDidMount() {
        this.btnNode = document.querySelector(`.ProductPage-cart-btn-${this.props.productId}[data-product-id='${this.props.productId}']`);
        this.watchedNode = document.querySelector(`.product-description[data-product-id='${this.props.productId}']`);
        this.timer = setInterval(
            () => this.tick(),
            3000
        );
    }
    componentWillUnmount() {
        clearInterval(this.timer);
    }
    
    animateVanish(vanisher) {
        let delta = Math.min((Date.now() - then) / (1000 / 60), 2);
        then = Date.now();
        const opacity = window.getComputedStyle(vanisher).getPropertyValue("opacity");
        if (opacity == 0.0) {
            this.watchedNode.removeChild(vanisher);
            this.vanishing = false;
            return;
        }
        vanisher.setAttribute("style", `opacity: ${opacity - (0.05 * delta)}`);
        requestAnimationFrame(
            () => this.animateVanish(vanisher)
        );
    }

    tick() {
        if (this.watchedNode.childElementCount == 2 || this.vanishing) {
            return
        }
        this.vanishing = true;
        const child = this.watchedNode.children[2];
        const message = child.innerText;
        const newValue = Number(message.split(" ")[1]);
        then = Date.now();
        requestAnimationFrame(
            () => this.animateVanish(child)
        );
        this.setState((state, props) => ({
            quantity: state.quantity + newValue
        }));
        this.btnNode.classList.remove("btn-disabled");
    }

    render() {
        return (
            <div
                style={{ visibility: this.state.quantity > 0 ? "visible" : "hidden" }}
                className="product-buttons-cart-indicator-text text-center">
                <strong>
                    {this.state.quantity}
                </strong> in your cart
            </div>
        )
    }
}

export default CartQuantityUpdater