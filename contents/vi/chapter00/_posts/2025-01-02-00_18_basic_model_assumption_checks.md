---
layout: post
title: "Bài 0.20: Kiểm tra giả định mô hình cơ bản"
chapter: '00'
order: 20
owner: Nguyen Le Linh
lang: vi
categories:
- chapter00
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn sẽ biết cách kiểm tra nhanh nhưng có hệ thống các giả định cốt lõi của mô hình (dạng phân phối, tính độc lập, cấu trúc sai số), nhận diện dấu hiệu sai mô hình (misspecification), và biến kết quả kiểm tra thành hành động cải tiến mô hình.

## 1) Giả định mô hình là gì và nằm ở đâu?

**Mỗi mô hình thống kê ngầm nói rằng dữ liệu được sinh từ một cơ chế nào đó, nhiễu có một cấu trúc nhất định, và quan hệ giữa biến đầu vào với biến đầu ra có một dạng hình học hoặc xác suất cụ thể.**

Trong thực hành, giả định thường xuất hiện ở 3 nơi. Thứ nhất là ở **likelihood**, tức dữ liệu thuộc họ phân phối nào như Gaussian, Poisson hay Binomial. Thứ hai là ở **mean structure**, tức quan hệ trung bình giữa $$x$$ và $$y$$ là tuyến tính, phi tuyến, hay có tương tác. Thứ ba là ở **noise structure**, nơi ta hỏi phương sai có hằng hay thay đổi theo mức dự báo, và dữ liệu có phụ thuộc theo thời gian hoặc theo nhóm hay không.

## 2) Bộ kiểm tra tối thiểu nên làm

### 2.1 Kiểm tra phân phối đầu ra

1. Vẽ histogram/density của $$y$$.
2. So sánh trực giác với likelihood đang chọn.
3. Tự hỏi: dữ liệu có bị lệch mạnh, có nhiều số 0, có biên tự nhiên (0-1) không?

Ví dụ, dữ liệu đếm có quá nhiều số 0 thường không phù hợp với Gaussian, còn dữ liệu tỷ lệ nằm trong $$[0,1]$$ đòi hỏi một mô hình tôn trọng miền giá trị đó thay vì dự báo ra ngoài khoảng hợp lệ.

### 2.2 Kiểm tra phần dư

Phần dư thường được viết:

$$
e_i = y_i - \hat y_i
$$

Ở đây, $$e_i$$ là **phần dư (residual)** của quan sát thứ $$i$$, tức độ chênh giữa giá trị quan sát thật $$y_i$$ và giá trị mô hình dự báo $$\hat y_i$$. Nếu $$e_i > 0$$ thì mô hình đang dự báo thấp hơn thực tế; nếu $$e_i < 0$$ thì mô hình đang dự báo cao hơn thực tế.

Đừng nhầm $$e_i$$ với $$\epsilon_i$$. Trong mô hình sinh dữ liệu, ta thường viết $$y_i = \mu_i + \epsilon_i$$, trong đó $$\epsilon_i$$ là **sai số thật nhưng không quan sát trực tiếp** của quá trình tạo dữ liệu. Còn $$e_i = y_i - \hat y_i$$ là **residual tính sau khi đã fit mô hình**, nên chỉ là phiên bản thực hành dùng để kiểm tra xem mô hình đang lệch khỏi dữ liệu như thế nào. Nếu mô hình hợp lý thì hành vi của $$e_i$$ có thể gần với hành vi của $$\epsilon_i$$, nhưng chúng không hoàn toàn trùng nhau vì $$\hat y_i$$ là giá trị ước lượng từ chính dữ liệu.

Kỳ vọng cơ bản của một mô hình tạm ổn là phần dư dao động quanh 0, không tạo ra xu hướng rõ ràng theo $$\hat y$$ hoặc theo $$x$$, và không để lộ những hình dạng có cấu trúc như đường cong, hình phễu, hay các cụm tách biệt theo nhóm.

![Residual check để nhìn xu hướng phần dư]({{ site.baseurl }}/img/chapter_img/chapter00/basic_model_residual_check.png)

*Hình 1a: Residual plot giúp nhìn nhanh xem phần dư có bám quanh 0 hay đang lộ ra cấu trúc bất thường.*

### 2.3 Kiểm tra outlier và điểm ảnh hưởng mạnh

Không phải outlier nào cũng "xấu". Chúng có thể là lỗi dữ liệu, trường hợp hiếm nhưng hợp lệ, hoặc tín hiệu cho thấy mô hình đang thiếu biến hay dùng sai likelihood.

Điều quan trọng là kiểm tra độ nhạy: bỏ/tái trọng số một vài điểm liệu kết luận có đổi đáng kể không.

![Fit tuyến tính và các điểm có thể là outlier]({{ site.baseurl }}/img/chapter_img/chapter00/basic_model_fit_outliers.png)

*Hình 1b: Quan sát đường fit cùng các điểm xa xu hướng chung giúp phát hiện outlier và điểm ảnh hưởng mạnh trước khi cập nhật mô hình.*

### 2.4 Kiểm tra giả định độc lập

Giả định độc lập dễ vỡ trong dữ liệu thực tế. Ta có thể gặp phụ thuộc theo **thời gian** do tự tương quan, theo **nhóm** như học sinh trong cùng lớp hoặc bệnh nhân trong cùng bệnh viện, và theo **không gian** khi các điểm đo gần nhau thường giống nhau hơn.

Nếu bỏ qua phụ thuộc, khoảng bất định thường bị đánh giá quá lạc quan (quá hẹp).

## 3) Bản đồ "dấu hiệu -> hành động"

Đây không phải là bảng "thấy A thì chắc chắn phải dùng B". Cách đúng là:

1. Nhìn dấu hiệu trong dữ liệu hoặc residual.
2. Suy ra giả định nào của mô hình đang bị nghi ngờ.
3. Chọn bản cập nhật nhỏ nhất nhưng đúng trọng tâm để kiểm tra lại.

Có thể đọc nhanh bản đồ này theo mẫu: **dấu hiệu -> nghi ngờ gì -> thử sửa theo hướng nào**.

**Residual có hình cong**

- Điều đó thường gợi ý mean structure đang sai: quan hệ trung bình giữa biến đầu vào và đầu ra không còn tuyến tính đơn giản.
- Hành động nên thử trước: thêm thành phần phi tuyến như `x^2`, `log(x)`, spline, hoặc thêm biến tương tác nếu nghi ngờ hiệu ứng của một biến phụ thuộc vào biến khác.

**Residual có dạng hình phễu**

- Điều đó thường gợi ý phương sai không hằng, tức mức nhiễu tăng theo giá trị dự báo.
- Hành động nên thử trước: đổi thang đo như `log(y)`, dùng likelihood phù hợp hơn với dữ liệu lệch/phương sai tăng, hoặc mô hình hóa phương sai thay đổi nếu bối cảnh yêu cầu.

**Xuất hiện nhiều giá trị cực đoan hơn mong đợi**

- Điều đó thường gợi ý likelihood hiện tại quá "mỏng đuôi", ví dụ Gaussian không chịu được outlier tốt.
- Hành động nên thử trước: kiểm tra lại lỗi dữ liệu, xem có thiếu biến quan trọng không, rồi cân nhắc likelihood heavy-tail như Student-t thay cho Gaussian.

**Dữ liệu đếm có quá nhiều số 0 hoặc phương sai lớn hơn trung bình rõ rệt**

- Điều đó thường gợi ý Poisson quá chặt so với dữ liệu thực.
- Hành động nên thử trước: dùng Negative Binomial khi có overdispersion; nếu số 0 quá nhiều do một cơ chế riêng, cân nhắc thêm zero-inflated hoặc hurdle model.

**Dữ liệu có cụm theo nhóm hoặc theo thời gian**

- Điều đó thường gợi ý giả định độc lập giữa các quan sát không còn hợp lý.
- Hành động nên thử trước: thêm cấu trúc phân cấp theo nhóm, random effects, hoặc mô hình hóa tương quan theo thời gian/thứ tự quan sát.

Nói ngắn gọn: đừng sửa mô hình theo tên gọi "hot", hãy sửa đúng giả định đang hỏng. Residual cong chủ yếu là vấn đề **mean structure**. Hình phễu là vấn đề **noise structure**. Quá nhiều số 0 hay đuôi dày thường là vấn đề **likelihood**. Phụ thuộc theo nhóm/thời gian là vấn đề **independence structure**.

## 4) Ví dụ dữ liệu thực tế: nêu rõ nguồn số liệu và suy luận

Để tránh tình trạng "nhận xét cảm tính", phần này dùng dữ liệu công khai có thể tái lập trực tiếp bằng Python (`seaborn.load_dataset`). Mỗi ví dụ đều đi theo cùng một chuỗi lập luận:

1. Nói rõ dữ liệu và câu hỏi đang muốn trả lời.
2. Chọn một baseline đơn giản để biết chính xác mình đang giả định điều gì.
3. Dùng số liệu mô tả hoặc residual để kiểm tra xem giả định đó có hợp lý không.
4. Chỉ sau khi nhìn thấy dấu hiệu sai mô hình thì mới đề xuất cập nhật.

### Ví dụ 1: Dữ liệu `diamonds` (giá kim cương)

**Nguồn dữ liệu**: `seaborn.load_dataset("diamonds")`, $$n=53{,}940$$ quan sát.

**Câu hỏi**: nếu chỉ bắt đầu với một predictor đơn giản là trọng lượng `carat`, thì mô hình nào có thể mô tả giá `price` một cách tạm ổn, và những giả định nào dễ hỏng nhất?

Ví dụ này hữu ích vì nó cho thấy một lỗi rất phổ biến trong dữ liệu thực: biến đầu ra dương, lệch phải, và độ biến động tăng lên khi giá trị trung bình tăng. Nếu ta fit thẳng một mô hình Gaussian tuyến tính trên thang giá gốc, ta thường sẽ gặp vấn đề ở cả **mean structure** lẫn **noise structure**.

**Một lát cắt nhỏ của dữ liệu để hình dung**: bảng dưới đây không phải dữ liệu tổng hợp, mà là 7 quan sát thật lấy từ các mốc khác nhau của phân phối giá sau khi sắp `price` tăng dần. Mục đích là giúp bạn thấy nhanh khi `carat` tăng thì `price` thường tăng mạnh, nhưng giá vẫn còn phụ thuộc vào `cut`, `color`, và `clarity`.

| Mốc trong phân phối giá | carat | cut | color | clarity | price (USD) |
| --- | ---: | --- | --- | --- | ---: |
| 0% | 0.23 | Ideal | E | SI2 | 326 |
| 10% | 0.31 | Ideal | H | VS2 | 646 |
| 30% | 0.42 | Premium | H | VS1 | 1087 |
| 50% | 0.58 | Ideal | F | VVS2 | 2401 |
| 70% | 1.02 | Ideal | I | VS2 | 4662 |
| 90% | 1.51 | Very Good | H | VS2 | 9821 |
| 98% | 2.43 | Very Good | H | SI2 | 16170 |

**Bước 1 - Kiểm tra phân phối đầu ra**: trước khi fit mô hình, ta hỏi câu rất cơ bản: `price` trên thang gốc có trông giống một biến gần Gaussian không?

Trên dữ liệu thực, `price` có `min=326`, `median=2401`, `max=18823`, độ lệch phải `skewness = 1.618`, và ngưỡng phân vị 95% là `13107.1`, tức đúng 5% quan sát nằm ở phía trên mức giá này.

Những con số đó nên được đọc như sau:

- `median=2401` nhưng `max=18823` cho thấy phía giá cao kéo dài rất xa so với vùng trung tâm.
- `skewness = 1.618` là dấu hiệu định lượng cho thấy phân phối lệch phải rõ rệt chứ không chỉ là "nhìn có vẻ lệch".
- Mốc 95% ở `13107.1` nhắc ta rằng chỉ một phần nhỏ quan sát nằm ở đuôi cao, nhưng chính phần nhỏ này có thể gây ảnh hưởng mạnh đến fit nếu ta dùng mô hình không phù hợp.

Nếu `price` thật sự gần Gaussian trên thang gốc, ta kỳ vọng histogram tương đối đối xứng quanh một vùng trung tâm và hai đuôi không quá chênh nhau. Dữ liệu thực không có hình dạng đó. Ngay từ bước này, ta đã có lý do để nghi ngờ rằng baseline Gaussian trên thang giá gốc sẽ gặp khó khăn.

![Diamonds price distribution]({{ site.baseurl }}/img/chapter_img/chapter00/basic_model_assumption_diamonds_distribution.png)

*Cách đọc hình: Hình này minh họa diamonds price distribution. Hãy đọc nhãn trục/chú thích trước, rồi so sánh xu hướng chính giữa các đường, cột hoặc nhóm điểm thay vì chỉ nhìn từng điểm lẻ.*
*Hình 2: Histogram giá kim cương (diamonds) với vạch q95, cho thấy phân phối lệch phải và đuôi cao.*

**Bước 2 - Fit baseline và kiểm tra residual**: để kiểm tra cụ thể giả định nào đang hỏng, ta vẫn nên fit một baseline đơn giản. Mục đích ở đây không phải tìm "mô hình cuối cùng", mà là tạo ra một điểm mốc rõ ràng để chẩn đoán.

Mô hình baseline:

$$
y_i \sim \mathcal{N}(\mu_i, \sigma), \quad \mu_i = \alpha + \beta\,\text{carat}_i
$$

Nếu viết theo dạng sai số quen thuộc, ta có thể hiểu tương đương là $$y_i = \mu_i + \epsilon_i$$ với $$\epsilon_i \sim \mathcal{N}(0,\sigma)$$. Mô hình này ngầm giả định hai điều lớn:

1. Giá trung bình tăng **tuyến tính** theo `carat`.
2. Mức độ dao động quanh đường trung bình có độ rộng gần như **không đổi** trên toàn bộ miền dự báo.

Sau khi fit mô hình xong, thứ ta đem đi kiểm tra trên biểu đồ không phải $$\epsilon_i$$ vì nó không quan sát được, mà là residual $$e_i = y_i - \hat y_i$$.

Chẩn đoán định lượng trên residual cho thấy:

- $$\mathrm{corr}(\lvert e_i \rvert, \hat y_i)=0.579$$ là mạnh và dương, nghĩa là fitted càng lớn thì độ lớn residual càng có xu hướng tăng.
- MAE của nhóm fitted thấp và cao lần lượt là `478.4` và `2059.1`, tức chênh nhau tới `4.30` lần.

Đây là một kết quả rất quan trọng. Nếu vấn đề chỉ là một vài outlier lẻ tẻ, ta có thể thấy vài điểm cực đoan nhưng không nhất thiết thấy độ rộng của residual tăng có hệ thống. Ngược lại, hai con số trên cho thấy sự gia tăng độ phân tán là **có cấu trúc**: mô hình dự báo càng cao thì sai số tuyệt đối càng lớn. Nói cách khác, giả định **đồng nhất phương sai** đang hỏng khá rõ.

Quan sát này cũng hợp với trực giác nghiệp vụ: sai khác 500 USD có thể lớn với viên giá 700 USD, nhưng lại không quá lớn với viên giá 10,000 USD. Trên thang giá gốc, mức nhiễu thường mang tính "tỷ lệ" hơn là "cộng thêm một lượng cố định".

![Diamonds residual vs fitted]({{ site.baseurl }}/img/chapter_img/chapter00/basic_model_assumption_diamonds_residuals.png)

*Cách đọc hình: Hình này minh họa diamonds residual vs fitted. Hãy đọc nhãn trục/chú thích trước, rồi so sánh xu hướng chính giữa các đường, cột hoặc nhóm điểm thay vì chỉ nhìn từng điểm lẻ.*
*Hình 3: Residual vs fitted của mô hình baseline trên diamonds; độ phân tán residual mở rộng khi fitted tăng (dấu hiệu heteroscedasticity).*

**Bước 3 - Cập nhật mô hình và kiểm tra lại**: cập nhật tốt không phải là cập nhật "phức tạp hơn", mà là cập nhật giải quyết đúng lỗi vừa quan sát được.

Mô hình cập nhật (ổn định hơn):

$$
\log y_i = \alpha + \beta_1\,\text{carat}_i + \beta_2\,\text{carat}_i^2 + \epsilon_i,
$$

với $$\epsilon_i$$ có thể xem gần Gaussian hơn trên thang log.

Vì sao cập nhật này hợp lý?

- Lấy `log(y)` giúp biến đầu ra dương và lệch phải trở nên "hiền" hơn, đồng thời biến sai khác theo tỷ lệ thành sai khác cộng tính dễ mô hình hóa hơn.
- Thêm `carat^2` cho phép quan hệ giữa trọng lượng và giá có độ cong, thay vì ép mọi thứ vào một đường thẳng.

Sau khi cập nhật mô hình, $$\mathrm{corr}(\lvert e_i \rvert, \hat y_i)$$ giảm từ `0.579` xuống `0.047`, còn tỉ lệ MAE cao/thấp giảm từ `4.30` xuống `1.16`.

Hai thay đổi này có ý nghĩa thực hành rất rõ:

- Tương quan gần 0 cho thấy residual không còn phình ra rõ rệt khi fitted tăng.
- Tỉ lệ MAE gần 1 cho thấy sai số ở vùng giá thấp và vùng giá cao đã cân bằng hơn nhiều.

Kết luận của ví dụ này không phải là "mô hình log-quadratic chắc chắn đúng", mà là: kiểm tra giả định đã chỉ ra rất cụ thể baseline sai ở đâu, và bản cập nhật được chọn đã sửa đúng những điểm hỏng đó bằng cùng bộ tiêu chí chẩn đoán.

---

### Ví dụ 2: Dữ liệu `taxis` (đếm số chuyến theo zone-ngày)

**Nguồn dữ liệu**: `seaborn.load_dataset("taxis")`.

**Câu hỏi**: nếu gom dữ liệu thành số chuyến theo từng `pickup_zone` và từng ngày, thì Poisson có phải là baseline hợp lý cho biến đếm `trips` hay không?

Ví dụ này hữu ích vì đây là kiểu bài toán đếm rất phổ biến. Với dữ liệu đếm, giả định cốt lõi nằm nhiều ở **likelihood** hơn là ở residual Gaussian. Do đó, ta ưu tiên kiểm tra xem Poisson đang ngầm nói gì về dữ liệu, rồi so sánh trực tiếp với thực tế.

**Cách tạo biến đếm**:

1. Giữ các chuyến có `pickup_borough = Manhattan`.
2. Gộp theo cặp `(pickup_zone, day)` để tạo biến đếm `trips`.
3. Điền đầy đủ mọi tổ hợp zone-ngày để bảo toàn các ngày có 0 chuyến.

Sau khi tổng hợp, có $$n=1953$$ ô quan sát zone-ngày. Mỗi ô lúc này là một biến đếm không âm: có ngày-zone không có chuyến nào, có ngày-zone rất ít chuyến, và cũng có ngày-zone bùng lên khá mạnh.

**Bước 1 - Kiểm tra giả định Poisson cơ bản**: với Poisson baseline, nếu $$Y \sim \mathrm{Poisson}(\lambda)$$ thì một hệ quả rất quan trọng là:

$$
\mathbb{E}[Y] = \mathrm{Var}(Y).
$$

Trên dữ liệu thực, ta có `mean(trips)=2.697`, `var(trips)=7.441`, nên tỉ lệ `var/mean = 2.76`.

Con số `2.76` nên được đọc như sau: độ phân tán thực tế lớn gần gấp 3 lần mức mà Poisson kỳ vọng khi cùng có trung bình 2.697. Đây không phải lệch nhỏ do ngẫu nhiên, mà là dấu hiệu rõ ràng của **overdispersion**.

Diễn giải trực giác: nếu mọi zone-ngày đều có cùng một cường độ phát sinh chuyến gần như nhau, Poisson có thể hợp lý. Nhưng dữ liệu thực thường có dị biệt mạnh giữa zone đông khách và zone ít khách, giữa ngày yên ắng và ngày nhộn nhịp. Dị biệt đó làm phương sai phình lên nhanh hơn Poisson cho phép.

![Taxis trip-count distribution]({{ site.baseurl }}/img/chapter_img/chapter00/basic_model_assumption_taxis_distribution.png)

*Cách đọc hình: Hình này minh họa taxis trip-count distribution. Hãy đọc nhãn trục/chú thích trước, rồi so sánh xu hướng chính giữa các đường, cột hoặc nhóm điểm thay vì chỉ nhìn từng điểm lẻ.*
*Hình 4: Phân phối số chuyến theo zone-ngày trong taxis, kèm thống kê mean, variance, và var/mean để nhận diện overdispersion.*

**Bước 2 - Kiểm tra phần zero và đuôi phải**: một ưu điểm lớn của Poisson là khi đã biết trung bình $$\lambda$$, nó không chỉ quyết định mean mà còn quyết định luôn xác suất của ngày có 0 chuyến và của các ngày rất bận. Vì thế, nếu Poisson sai ở các xác suất này, ta biết ngay likelihood đang không đủ linh hoạt.

Tỉ lệ zero quan sát là `P(Y=0)=0.245`, trong khi Poisson với $$\lambda=2.697$$ chỉ dự báo `P(Y=0)=e^{-\lambda}=0.067`.

Nói cách khác, dữ liệu có số ngày-zone bằng 0 nhiều gấp khoảng `0.245 / 0.067 \approx 3.7` lần so với dự báo Poisson.

Ở đuôi phải, xác suất quan sát được `P(Y>=10)=0.0261`, trong khi Poisson chỉ dự báo `P(Y>=10)=0.00050`.

Ở đây sai khác còn mạnh hơn nữa: xác suất ngày-zone rất bận trong dữ liệu lớn gấp khoảng `52` lần so với Poisson.

Đây là điểm rất đáng chú ý. Dữ liệu đang có đồng thời:

- quá nhiều ngày-zone im ắng,
- và cũng quá nhiều ngày-zone bận rộn.

Poisson với một tham số trung bình cố định không làm tốt cả hai đầu này cùng lúc. Nó quá "hẹp": khi cố khớp trung bình, nó sẽ thiếu cả zero lẫn tail.

![Observed vs model implied probabilities on taxis]({{ site.baseurl }}/img/chapter_img/chapter00/basic_model_assumption_taxis_probabilities.png)

*Cách đọc hình: Hình này minh họa observed vs model implied probabilities on taxis. Hãy đọc nhãn trục/chú thích trước, rồi so sánh xu hướng chính giữa các đường, cột hoặc nhóm điểm thay vì chỉ nhìn từng điểm lẻ.*
*Hình 5: So sánh xác suất quan sát với xác suất suy ra từ Poisson và Negative Binomial cho hai thống kê mục tiêu: $$P(Y=0)$$ và $$P(Y\ge 10)$$.*

**Bước 3 - Cập nhật và kiểm tra lại**: khi dữ liệu đếm có overdispersion, Negative Binomial là một cập nhật rất tự nhiên vì nó cho phép phương sai lớn hơn trung bình.

Ước lượng Negative Binomial theo moment matching với tham số phân tán $$k=1.534$$ cho dự báo `P(Y=0)=0.211`, gần hơn nhiều với mức 0.245 quan sát được, và cho `P(Y>=10)=0.0279`, gần sát với mức 0.0261 của dữ liệu.

Diễn giải trực giác của Negative Binomial là: thay vì giả sử mọi zone-ngày có cùng một cường độ sinh chuyến cố định, ta cho phép cường độ đó biến thiên nhiều hơn giữa các hoàn cảnh khác nhau. Chính độ biến thiên ẩn này làm phân phối đếm có đuôi dày hơn và nhiều zero hơn.

Điều quan trọng ở đây là ta không chọn Negative Binomial vì "đây là mô hình hay dùng", mà vì nó sửa đúng chỗ Poisson thất bại:

- phương sai lớn hơn trung bình,
- zero nhiều hơn dự báo,
- và đuôi phải nặng hơn dự báo.

Kết luận của ví dụ này là: chỉ riêng kiểm tra giả định bằng thống kê mô tả đã đủ cho thấy Poisson baseline không phù hợp, và Negative Binomial là một cập nhật có cơ sở dữ liệu rõ ràng.

---

### Điều cần rút ra từ hai ví dụ

Hai ví dụ trên nhấn mạnh bốn bài học thực hành rất quan trọng:

1. Đừng bắt đầu bằng mô hình phức tạp; hãy bắt đầu bằng một baseline đủ đơn giản để bạn biết mình đang giả định gì.
2. Đừng kết luận bằng mắt thường; hãy gắn mỗi nhận xét với một con số cụ thể như `skewness`, `var/mean`, tương quan của residual, hay xác suất zero và tail.
3. Đừng cập nhật mô hình một cách cảm tính; hãy sửa đúng giả định đang hỏng: ví dụ log-transform và thêm độ cong khi sai ở thang đo/mean structure, hoặc đổi sang Negative Binomial khi sai ở likelihood đếm.
4. Đừng chỉ nói mô hình mới "trông tốt hơn"; hãy dùng lại chính các chỉ số chẩn đoán cũ để kiểm tra xem mô hình mới đã cải thiện thật hay chưa.

## 5) Quy trình 15 phút trước khi tin kết quả

1. Xem phân phối của biến mục tiêu.
2. Fit mô hình đơn giản làm baseline.
3. Vẽ residual vs fitted và residual vs predictor chính.
4. Tìm điểm ảnh hưởng mạnh và kiểm tra độ nhạy kết luận.
5. Kiểm tra dấu hiệu phụ thuộc theo thời gian/nhóm.
6. Ghi lại 1-2 giả định có rủi ro cao nhất.
7. Cập nhật mô hình rồi so sánh lại.

Mục tiêu là giảm rủi ro suy luận sai, không phải làm đủ mọi biểu đồ có thể.

## 6) Sai mô hình không phải thất bại, mà là tín hiệu cập nhật

Trong tư duy Bayesian workflow:

1. Đề xuất mô hình,
2. Fit mô hình,
3. Kiểm tra hệ quả dự báo và giả định,
4. Cải tiến mô hình.

Mục tiêu không phải "chứng minh mô hình đúng", mà là làm mô hình phù hợp hơn với dữ liệu và câu hỏi thực tế.

## Tóm tắt nhanh

1. Mô hình luôn đi kèm giả định.
2. Giả định sai có thể làm kết luận sai.
3. Bộ kiểm tra tối thiểu gồm: phân phối, residual, outlier/influence, phụ thuộc.
4. Dấu hiệu sai mô hình phải dẫn tới hành động chỉnh likelihood/cấu trúc mô hình.
5. Misspecification là thông tin để cải thiện mô hình, không phải "thất bại".

## Câu hỏi tự luyện

1. Nêu một tình huống vi phạm giả định độc lập trong dữ liệu thực và đề xuất cách sửa mô hình.
2. Vì sao kiểm tra residual vs fitted giúp phát hiện sai dạng hàm trung bình?
3. Nếu có outlier mạnh, bạn sẽ phân biệt "lỗi dữ liệu" và "tín hiệu thật" bằng cách nào?
4. Chọn một bài toán bạn từng làm và liệt kê 2 giả định rủi ro nhất của mô hình đó.

## Tài liệu tham khảo

- Gelman, A., et al. (2013). *Bayesian Data Analysis*.
- McElreath, R. (2020). *Statistical Rethinking*.

---

*Bài học tiếp theo: [0.21 Mô phỏng để kiểm tra trực giác thống kê](/vi/chapter00/simulation-for-statistical-intuition/)*
