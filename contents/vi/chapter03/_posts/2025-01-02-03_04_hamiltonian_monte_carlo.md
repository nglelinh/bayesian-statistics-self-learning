---
layout: post
title: "Bài 3.4: Hamiltonian Monte Carlo - Tăng Tốc MCMC với Gradient"
chapter: '03'
order: 4
owner: Nguyen Le Linh
lang: vi
categories:
- chapter03
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn cần hiểu vì sao Hamiltonian Monte Carlo (HMC) thường hiệu quả hơn Metropolis-Hastings dạng random walk. Bạn không cần thuộc chi tiết vật lý ngay lập tức, nhưng cần nắm trực giác quan trọng: HMC dùng gradient để đi có hướng trong không gian posterior, nhờ đó khám phá nhanh hơn và đỡ mắc kẹt hơn.

> **Ví dụ mini.** Nếu Metropolis-Hastings giống như người bịt mắt dò từng bước ngắn trên bản đồ, thì HMC giống như người vừa nhìn được độ dốc địa hình vừa có quán tính để lướt đi. Hai người cùng tìm vùng posterior cao, nhưng cách di chuyển hoàn toàn khác nhau.
>
> **Câu hỏi tự kiểm tra.** Vì sao thông tin về độ dốc của log-posterior lại có thể giúp sampler hiệu quả hơn rất nhiều?

## 1. Vì sao ta cần HMC?

Metropolis-Hastings rất quan trọng để xây trực giác, nhưng nó có một hạn chế lớn:

- thường di chuyển kiểu random walk.

Điều đó có nghĩa là:

- bước đi ngắn và dò dẫm,
- dễ bị autocorrelation cao,
- rất chậm khi posterior nhiều chiều hoặc có tương quan mạnh.

Trong các mô hình Bayes hiện đại:

- hồi quy nhiều biến,
- mô hình phân cấp,
- mô hình có hàng chục hay hàng trăm tham số,

random walk có thể trở nên quá chậm.

HMC ra đời để giải quyết chính vấn đề đó.

## 2. Trực giác cốt lõi của HMC

Thay vì chỉ biết “điểm hiện tại có posterior cao hay thấp”, HMC còn nhìn được:

- **gradient** của log-posterior,
- tức là hướng dốc nhất để posterior tăng lên.

Bạn có thể tưởng tượng posterior như một địa hình:

- vùng posterior cao là thung lũng năng lượng thấp,
- vùng posterior thấp là các khu vực “cao năng lượng”.

HMC đặt một “hạt” trong địa hình đó rồi cho nó:

- một động lượng ban đầu,
- và một lực đẩy theo gradient.

Hạt này không bò từng bước ngắn như MH, mà lướt qua không gian tham số theo những quỹ đạo dài và mượt hơn.

![Random walk và HMC đi khác nhau thế nào]({{ site.baseurl }}/img/chapter_img/chapter03/random_walk_vs_hmc_directed.png)

## 3. HMC lấy ý tưởng từ vật lý như thế nào?

Bạn không cần quá sợ phần này. Điều quan trọng nhất chỉ là cách đổi tên.

### Position

Đây là tham số $$\theta$$ mà ta muốn lấy mẫu.

### Momentum

Đây là một biến phụ thêm $$p$$, đóng vai trò như “động lượng” để giúp chuỗi không đi giật cục.

### Hamiltonian

Đây là tổng của:

- năng lượng thế: liên quan tới posterior,
- động năng: liên quan tới momentum.

Về trực giác, HMC biến bài toán lấy mẫu thành bài toán:

- cho một vật chuyển động trong một trường lực được tạo bởi posterior.

Nghe vật lý, nhưng mục tiêu cuối cùng vẫn là lấy mẫu Bayes.

## 4. Gradient giúp gì cho ta?

Gradient cho biết:

- đi về phía nào thì posterior tăng nhanh,
- đi về phía nào thì posterior giảm.

Thông tin này cực kỳ quý vì nó giúp sampler:

- tránh đi lang thang vô hướng,
- bám tốt hơn theo hình dạng posterior,
- đặc biệt hiệu quả khi posterior có hình cong, dài hoặc tương quan mạnh.

![HMC so với MH trong posterior tương quan mạnh]({{ site.baseurl }}/img/chapter_img/chapter03/hmc_vs_mh.png)

## 5. Một cách hình dung rất thực tế

Hãy nghĩ tới hai cách khám phá một thành phố lạ.

### Metropolis-Hastings

- đi bộ từng bước ngắn,
- rẽ trái rẽ phải gần như ngẫu nhiên,
- nên rất lâu mới hiểu được cấu trúc toàn thành phố.

### HMC

- đi bằng xe đạp trên bản đồ có chỉ dẫn độ dốc,
- có quán tính nên không phải dừng ở mỗi bước,
- và biết nên lao về hướng nào hiệu quả hơn.

Đó là khác biệt về hiệu suất.

## 6. Leapfrog: HMC mô phỏng chuyển động như thế nào?

Để dùng ý tưởng vật lý vào máy tính, HMC mô phỏng chuyển động bằng một thủ tục số học gọi là **leapfrog integrator**.

Bạn không cần nhớ toàn bộ công thức, chỉ cần hiểu:

- momentum được cập nhật một phần,
- position được cập nhật,
- rồi momentum lại được cập nhật tiếp.

Vòng lặp này tạo ra một quỹ đạo tương đối ổn định trong không gian tham số.

Lý do leapfrog được ưa chuộng là vì nó:

- khá bền về mặt số học,
- gần như bảo toàn năng lượng,
- và dẫn tới acceptance rate cao hơn nhiều so với MH.

## 7. Vì sao HMC thường chấp nhận proposal tốt hơn?

Trong MH random walk, proposal thường “vô hướng”, nên rất dễ rơi vào vùng posterior thấp và bị từ chối.

Trong HMC:

- proposal được sinh ra theo quỹ đạo dùng gradient,
- nên nó thường bám vào các vùng posterior hợp lý hơn,
- nhờ đó tỉ lệ chấp nhận thường cao.

Hệ quả:

- ít bước bị lãng phí,
- ít đứng yên,
- hiệu quả thống kê tốt hơn.

## 8. HMC đặc biệt mạnh khi posterior nhiều chiều

Ở không gian ít chiều, MH có thể vẫn tạm ổn. Nhưng khi số tham số tăng:

- posterior thường có tương quan,
- các vùng khối lượng cao có hình rất dài, rất cong,
- random walk trở nên cực kỳ kém hiệu quả.

HMC lại rất hợp với các hình dạng đó vì:

- gradient dẫn đường,
- quán tính giúp đi xa hơn,
- và quỹ đạo dài giúp giảm random walk behavior.

Đây là lý do HMC trở thành nền tảng của các công cụ hiện đại như Stan và PyMC.

## 9. HMC không phải phép màu

HMC mạnh, nhưng không phải vô địch trong mọi hoàn cảnh.

Nó cần:

- posterior đủ trơn để tính gradient,
- mô hình viết đúng,
- tuning step size hợp lý,
- warm-up đủ để thích nghi.

Nếu posterior rất gồ ghề, rời rạc hoặc có cấu trúc không khả vi, HMC có thể không còn là lựa chọn tốt nhất.

## 10. NUTS: vì sao ta thường không chạy HMC “tay”?

HMC cơ bản cần người dùng chọn:

- step size bao nhiêu,
- số leapfrog steps bao nhiêu.

Chọn không khéo thì:

- đi quá ít  $$\rightarrow$$ chưa tận dụng được lợi thế,
- đi quá nhiều  $$\rightarrow$$ tốn tính toán không cần thiết.

NUTS (No-U-Turn Sampler) ra đời để tự động hóa phần này:

- nó tự điều chỉnh đường đi,
- dừng khi bắt đầu quay đầu vô ích,
- và thường là thứ bạn dùng trong PyMC chứ không phải HMC “thuần” bằng tay.

## 11. Tại sao người học vẫn cần hiểu HMC?

Vì nếu chỉ dùng PyMC như black box, bạn sẽ khó hiểu:

- vì sao sampler này tốt,
- vì sao gradient lại quan trọng,
- vì sao tuning/warm-up cần thiết,
- và vì sao mô hình có thể chạy chậm hoặc báo divergence.

Hiểu HMC giúp bạn:

- hiểu tinh thần của NUTS,
- hiểu vì sao sampler hiện đại mạnh,
- và đọc diagnostics sau này tốt hơn nhiều.

> **3 ý cần nhớ.**
> 1. HMC dùng gradient để di chuyển có hướng trong không gian posterior, thay vì random walk mù mờ như MH.
> 2. Nhờ có quán tính và thông tin độ dốc, HMC thường khám phá posterior nhanh hơn và ít autocorrelation hơn.
> 3. Trong thực hành, bạn thường dùng NUTS thay vì HMC thủ công, nhưng trực giác của HMC vẫn rất quan trọng để hiểu sampler hiện đại.

## Câu hỏi tự luyện

1. Vì sao MH dạng random walk thường kém hiệu quả trong posterior nhiều chiều?
2. Gradient cho HMC biết điều gì mà MH không có?
3. Hãy giải thích bằng lời vì sao HMC thường có acceptance rate tốt hơn.
4. Vì sao NUTS lại phổ biến hơn HMC thủ công trong các thư viện hiện đại?

## Tài liệu tham khảo

- Neal, R. M. (2011). MCMC using Hamiltonian dynamics.
- Betancourt, M. A Conceptual Introduction to Hamiltonian Monte Carlo.
- Gelman, A. et al. *Bayesian Data Analysis* (3rd ed.), Chapter 11.

---

*Bài học tiếp theo: [3.5 MCMC Diagnostics - Đảm bảo Chất lượng Mẫu](/vi/chapter03/mcmc-diagnostics/)*
