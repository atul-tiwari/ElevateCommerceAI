-- ElevateCommerceAI.amazon_product_lists definition

CREATE TABLE `amazon_product_lists` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `asin` varchar(100) NOT NULL,
  `product_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `url` varchar(100) NOT NULL,
  `keyword` varchar(100) DEFAULT NULL,
  `rating` decimal(10,0) DEFAULT NULL,
  `reviews` int DEFAULT NULL,
  `position` int DEFAULT NULL,
  `page_no` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=181 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;