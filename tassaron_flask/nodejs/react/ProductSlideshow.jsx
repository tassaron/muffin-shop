/* Adapted from example code in the react-slideshow-image documentation */
import React, { Component } from "react";
import { Slide } from "react-slideshow-image";

class ProductSlideshow extends Component {
    constructor(props) {
        super();
        this.slideRef = React.createRef();
        this.state = {
            current: 0
        };
    }

    render() {
        const properties = {
            duration: 6000,
            autoplay: true,
            transitionDuration: 600,
            arrows: false,
            infinite: true,
            easing: "ease",
            indicators: false,
        };

        if (this.props.slideImages.length == 1) {
            return <img className="lazy" src={this.props.slideImages[0]} alt={this.props.productName} />
        } else {
            return (
                <div className="ProductSlideshow">
                    <div className="slide-container">
                        <Slide ref={this.slideRef} {...properties}>
                            {this.props.slideImages.map((each, index) => (
                                <div draggable onDragStart={(e) => e.preventDefault()} key={index} className="each-slide">
                                    <img className="lazy" src={each} alt={this.props.productName} />
                                </div>
                            ))}
                        </Slide>
                    </div>
                </div>
            )
        }
    }
}

export default ProductSlideshow;
