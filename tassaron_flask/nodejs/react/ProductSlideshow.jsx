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
        const styles = [];
        for (let i=0; i < this.props.slideImages.length; i++) {
            styles.push({
                background: `black url(${this.props.slideImages[i]})`,
                backgroundRepeat: "no-repeat",
                backgroundSize: "cover",
                backgroundPosition: "bottom",
                height: "400px"
            });
        }

        if (this.props.slideImages.length == 1) {
            return (
                <div className="lazy" style={styles[0]} alt={this.props.productName} />
            )
        } else {
            return (
                <div className="ProductSlideshow">
                    <div className="slide-container">
                        <Slide ref={this.slideRef} {...properties}>
                            {
                                this.props.slideImages.map(
                                    (_, index) => (
                                        <div draggable onDragStart={(e) => e.preventDefault()} key={index} className="each-slide">
                                            <div className="lazy" style={styles[index]} alt={this.props.productName} />
                                        </div>
                                    )
                                )
                            }
                        </Slide>
                    </div>
                </div>
            )
        }
    }
}

export default ProductSlideshow;
