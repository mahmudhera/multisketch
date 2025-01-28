# multisketch
Here, we investigate if we take an average of multiple fracminhash containments and use the average as an estimate for the true containment -- does this result in a better estimator?

Theoretically, if these individual containments are independent from each other (there is no co-variance); then it can be shown that indeed the newly hypothesized estimator will be better.

In this repo, I am trying to see if indeed this is the case.


```
python main.py --scale_factor 0.01 --n_iter 500 --size1 100000 --size2 200000 --num_multisketches 4 --seed 7

True containment: 0.01005030150904527
Average containment (classic): 0.010111848698466474
Standard deviation from true (classic): 0.003317656413749616

Average containment (multisketch): 0.01018914776141325
Standard deviation from true (multisketch): 0.003312806708564233
```

This is an example, that shows that the new estimator (here, we refer to this using "multisketch") has an overall standard deviation of 0.003313; whereas the traditional fracminhash containment estimator (referred to as "classic" here) has an overall standard deviation of 0.00318.

This makes me suspect that there may be some possibility that this estimator may be better.

But, I am not certain (yet). And this is only just one single experiment.