/* Adapted from example code in the react-slideshow-image documentation */
import React, { Component } from "react";
import { Slide } from "react-slideshow-image";

class ProductSlideshow extends Component {
  constructor() {
    super();
    this.slideRef = React.createRef();
    this.back = this.back.bind(this);
    this.next = this.next.bind(this);
    this.state = {
      current: 0
    };
  }

  back() {
    this.slideRef.current.goBack();
  }

  next() {
    this.slideRef.current.goNext();
  }

  render() {
    const properties = {
      duration: 5000,
      autoplay: true,
      transitionDuration: 600,
      arrows: true,
      infinite: true,
      easing: "ease-in",
      //cssClass: "product-image-slider",
      indicators: false,
      //indicators: (i) => <div className="indicator">{i + 1}</div>
    };
    const slideImages = [
      "static/img/client/the_rainbow_farm/tomato_party.jpg",
      "static/img/client/the_rainbow_farm/zucchini_party.jpg",
      "static/img/client/the_rainbow_farm/pepper_party.jpg",
    ];

    return (
      <div className="ProductSlideshow">
        <div className="slide-container">
          <Slide ref={this.slideRef} {...properties}>
            {slideImages.map((each, index) => (
              <div key={index} className="each-slide">
                <img className="lazy" src={each} alt="sample" />
              </div>
            ))}
          </Slide>
        </div>
      </div>
    );
  }
}

export default ProductSlideshow;
